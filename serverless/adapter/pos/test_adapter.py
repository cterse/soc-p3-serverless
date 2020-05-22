from .adapter import *
from boto3.dynamodb.conditions import Key, Attr

# This file is for testing the adapter with pytest

req_label_schema = {"name": "RequestLabel",
                    "from": "Merchant",
                    "to": "Labeler",
                    "keys": ["orderID"],
                    "parameters": ["orderID", "address"],
                    "outs": ["orderID", "address"],
                    "ins": [],
                    "nils": []}

labeled_schema = {"name": "Labeled",
                  "from": "Labeler",
                  "to": "Packer",
                  "keys": ["orderID"],
                  "parameters": ["orderID", "address", "label"],
                  "outs": ["label"],
                  "ins": ["orderID", "address"],
                  "nils": []}

protocol = {
    "messages": [req_label_schema, labeled_schema]
}

request_label_1 = {
    "orderID": 1,
    "address": "Lancaster"
}

labeled_1 = {
    "orderID": 1,
    "address": "Lancaster",
    "label": "random-label"
}


def test_match_schema():
    assert match_schema(protocol["messages"],
                        request_label_1) == req_label_schema
    assert match_schema(protocol["messages"],
                        labeled_1) == labeled_schema


req_label_1_key_cond = Key('orderID').eq(1)


def test_build_key_condition():
    assert req_label_1_key_cond == key_condition(
        req_label_schema, request_label_1)
