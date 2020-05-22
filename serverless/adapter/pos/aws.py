import boto3
import os

offline = os.getenv('IS_OFFLINE')


def lambda_client():
    endpoint_url = 'http://localhost:3002/' if offline else None
    return boto3.client('lambda', endpoint_url=endpoint_url)


def dynamo_table(name):
    endpoint_url = 'http://localhost:8000/' if offline else None
    dynamodb = boto3.resource('dynamodb', endpoint_url=endpoint_url)
    return dynamodb.Table(name)
