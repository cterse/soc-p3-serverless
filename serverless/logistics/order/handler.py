import json
import boto3
import os
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Orders')

####################
def writeToDynamo(event, context):
    print('Generating new DynamoDB record')
    
    orderID = json.loads(event["body"]).get("orderID")
    address = json.loads(event["body"]).get("address")
    items = json.loads(event["body"]).get("items")
    
    entry = {
      "orderID": orderID,
      "address": address,
      "items": item
    }
    
    #Creating new record in DynamoDB table
    table.put_item(Item=entry)
    
    response = {
        "statusCode": 200,
        "body": json.dumps(entry)
    }

    return response
