import logging
import json
from collections import OrderedDict
from .aws import dynamo_table, lambda_client
from boto3.dynamodb.conditions import Key, Attr

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT, level="DEBUG")
logger = logging.getLogger('pos')


def match_schema(schemas, message):
    for schema in schemas:
        # find schema with exactly the same parameters (except nils, which should not be bound)
        if not set(schema['ins']).union(schema['outs']).symmetric_difference(message.keys()):
            return schema


def key_condition(schema, message):
    # initialize condition with the first key
    cond = Key(schema["keys"][0]).eq(message[key])
    # if there are any more keys, extend the condition using 'and'
    for key in schema['keys'][1:]:
        cond = cond & Key(key).eq(message[key])
    return cond


def check_dependencies(schema, history):
    """
    Make sure that all in parameters are bound by some message in the history
    """
    return all(any(h.get(p) for h in history) for p in schema['ins'])


def check_integrity(message, history):
    """
    Make sure message is compatible with history.
    Each message in history should have the same key values.

    Returns true if there are no messages in the history with contradictory bindings for any of the parameters.
    """
    # may not the most efficient algorithm for large histories
    # might be better to ask the database to find messages that don't match
    return not any(h.get(p) and message[p] != h[p]
                   for p in message.keys()
                   for h in history
                   if p in h.keys())


def check_outs(schema, message, history):
    """
    Make sure none of the outs have been bound.
    Only use this check if the message is being sent.
    """
    return not any(m.get(p)
                   for m in history
                   for p in message.keys())


class Adapter:
    def __init__(self, role, protocol, configuration, history_table_name):
        """
        Initialize the PoS adapter.

        role: name of the role being implemented
        protocol: a protocol specification
          {messages: [{keys, name, parameters, ins, outs, nils}], keys, name}
        configuration: a dictionary of roles to endpoint URLs
        history_table_name: the name of the DynamoDB table to use for storing message history
        """
        self.role = role
        self.protocol = protocol
        self.configuration = configuration

        self.db = dynamo_table(history_table_name)

    def get_enactment(self, schema, message):
        """
        Get all of the messages that match the keys of a message, as specified by schema
        """
        response = self.db.query(
            KeyConditionExpression=key_condition(schema, message)
        )
        return response['Items']

    def get_schema(self, message):
        return match_schema([schema for schemas in self.protocol['messages']
                             if schema['recipient'] == self.role],
                            message)

    def receive(self, event, context):
        message = json.loads(event['body'])

        schema = self.get_schema(message)
        if not schema:
            return {
                "statusCode": 500,
                "body": "Message does not match any schemas: " + json.dumps(message)
            }

        history = self.get_history(schema)

        if check_integrity(message, history):
            self.store(message)
            self.handle(schema, message)
            return {
                "statusCode": 200,
                "body": json.dumps(message)
            }
        else:
            return {
                "statusCode": 500,
                "body": 'Message does not satisfy integrity: ' + json.dumps(message)
            }

    def store(self, message):
        """Insert a message, represented as a dictionary
        E.g.: {"orderID": 1, "address": "Lancaster"}
        """
        # TODO insert message in history table

    def send(self, message):
        """
        Send a message by posting to the recipient's http endpoint,
        after checking for correctness, and storing the message.
        """
        schema = self.get_schema(message)
        if not schema:
            return
        history = self.get_history(schema)

        if check_dependencies(schema, history) \
           and check_integrity(message, history) \
           and check_outs(message, history):
            self.store(message)
            # TODO send message via http
