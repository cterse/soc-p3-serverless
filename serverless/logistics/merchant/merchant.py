import pos
import json
import yaml
from decimal import Decimal
import os

name = "Merchant"

with open("logistics.json") as stream:
    protocol = json.load(stream)
with open("configuration.yml") as conf:
    configuration = yaml.safe_load(conf)

adapter = pos.Adapter(name, protocol, configuration, 'MerchantHistory')


def translate_dynamo(obj):
    result = {}
    for k in obj:
        type = list(obj[k].keys())[0]
        if type == "N":
            result[k] = int(obj[k]["N"])
        else:
            result[k] = obj[k][type]
    return result


def handle_order(event, context):
    """
    Handle a stream event from DynamoDB.
    Receives a newly submitted order from the customer, and sends RequestLabel and RequestWrapping messages.
    """
    for record in event["Records"]:
        order = translate_dynamo(record["dynamodb"]["NewImage"])

        print("Received order: {}".format(order))
        request_label = {
            "orderID": order["orderID"],
            "address": order["address"]
        }
        print("Sending RequestLabel: {}".format(request_label))
        ok, msg = adapter.send("Labeler", request_label)
        if not ok:
            print(msg)

        for i, item in enumerate(order["items"].split(',')):
            request_wrapping = {
                "orderID": order["orderID"],
                "itemID": i,
                "item": item
            }
            print("Sending RequestWrapping: {}".format(request_wrapping))
            ok, msg = adapter.send("Wrapper", request_wrapping)
            if not ok:
                print(msg)


@adapter.sent(protocol['messages']['RequestLabel'])
def handleRequestLabel(message, enactment):
    print("RequestLabel sent: " + json.dumps(message))


@adapter.sent(protocol['messages']['RequestWrapping'])
def handleRequestWrapping(message, enactment):
    print("RequestWrapping sent: " + json.dumps(message))


@adapter.received(protocol['messages']['RequestWrapping'])
def handlePacked(message, enactment):
    print("An item has been successfully packed: " + json.dumps(message))


def lambda_handler(*args):
    adapter.handler(*args)
