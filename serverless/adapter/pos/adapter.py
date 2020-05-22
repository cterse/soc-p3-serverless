import logging
import json
import requests
from collections import OrderedDict
from .aws import dynamo_table, lambda_client
from boto3.dynamodb.conditions import Key, Attr
import datetime

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT, level="DEBUG")
logger = logging.getLogger('pos')


def now():
    return datetime.datetime.utcnow().isoformat()


def match_schema(schemas, message):
    for schema in schemas:
        # find schema with exactly the same parameters (except nils, which should not be bound)
        if not set(schema['ins']).union(schema['outs']).symmetric_difference(message.keys()):
            return schema


def check_integrity(message, enactment):
    """
    Make sure message is consistent with an enactment.
    Each message in enactment should have the same keys.

    Returns true if the parameters in the message are consistent with all messages in the enactment.
    """
    # may not the most efficient algorithm for large histories
    # might be better to ask the database to find messages that don't match
    return all(message[p] == m[p]
               for p in message.keys()
               for m in enactment
               if p in m)


def check_outs(schema, enactment):
    """
    Make sure none of the outs have been bound.
    Only use this check if the message is being sent.
    """
    return not any(m.get(p)
                   for m in enactment
                   for p in schema['outs'])


class Adapter:
    def __init__(self, role, protocol, configuration, history_table_name):
        """
        Initialize the PoS adapter.

        role: name of the role being implemented
        protocol: a protocol specification
          {name, keys, messages: [{name, from, to, parameters, keys, ins, outs, nils}]}
        configuration: a dictionary of roles to endpoint URLs
          {role: url}
        history_table_name: the name of the DynamoDB table to use for storing message history
        """
        self.role = role
        self.protocol = protocol
        self.configuration = configuration
        self.handlers = {}

        self.db = dynamo_table(history_table_name)

    def get_enactment(self, schema, message):
        """
        Get all of the messages that match the keys of a message, as specified by schema
        """
        keys = schema['keys']

        # we're using the first key as the partition key
        key_exp = Key(keys[0]).eq(message[keys[0]])

        # any other keys are just attributes; need a filter expression
        if len(keys) > 1:
            f = None
            for k in keys[1:]:
                exp = Attr(k).not_exists() | Attr(k).eq(message[k])
                f = f & exp if f else exp

            response = self.db.query(KeyConditionExpression=key_exp,
                                     FilterExpression=f)
        else:
            response = self.db.query(KeyConditionExpression=key_exp)

        return response['Items']

    def get_schema(self, to, message):
        return match_schema([schema for schema in self.protocol['messages']
                             if schema['to'] == to],
                            message)

    def receive(self, message):
        schema = self.get_schema(self.role, message)
        if not schema:
            return {
                "statusCode": 500,
                "body": "Message does not match any schema: " + json.dumps(message)
            }

        enactment = self.get_enactment(schema, message)

        if check_integrity(message, enactment):
            self.store(message)
            self.handle_message(schema, message, enactment)
            return {
                "statusCode": 200,
                "body": json.dumps(message)
            }
        else:
            return {
                "statusCode": 500,
                "body": 'Message does not satisfy integrity: ' + json.dumps(message)
            }

    def handler(self, event, context):
        message = json.loads(event['body'])
        return self.receive(message)

    def store(self, message):
        """Insert a message, represented as a dictionary
        E.g.: {"orderID": 1, "address": "Lancaster"}
        """
        message = message.copy()
        time = now()
        message["_time"] = time
        self.db.put_item(Item=message)
        return time

    def check_dependencies(self, schema, message):
        """
        Make sure that all 'in' parameters are bound and matched by some message in the history
        """
        for p in schema['ins']:
            results = self.db.scan(
                Select='COUNT',
                FilterExpression=Attr(p).eq(message[p])
            )
            if not results["Count"] > 0:
                return False
        return True

    def send(self, to, message):
        """
        Send a message by posting to the recipient's http endpoint,
        after checking for correctness, and storing the message.
        """
        schema = self.get_schema(to, message)
        if not schema:
            return False, "Message doesn't match any schema"
        enactment = self.get_enactment(schema, message)

        if check_outs(schema, enactment) \
           and check_integrity(message, enactment) \
           and self.check_dependencies(schema, message):
            self.store(message)
            self.handle_message(schema, message, enactment)
            requests.post(self.configuration[to],
                          data=message
                          )
            return True, message

    def message(self, schema):
        """
        Decorator for declaring message handlers.

        Example:
        @adapter.message(MessageSchema)
        def handle_message(message, enactment):
            'do stuff'
        """
        def register_handler(handler):
            self.handlers[json.dumps(schema, separators=(',', ':'))] = handler
        return register_handler

    def handle_message(self, schema, message, enactment):
        """
        Dispatch user-specified handler for schema, passing message and enactment.
        """
        handler = self.handlers.get(json.dumps(schema, separators=(',', ':')))
        if handler:
            handler(message, enactment)
