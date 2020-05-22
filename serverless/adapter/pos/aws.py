import boto3
import os


def lambda_client():
    offline = os.getenv('IS_OFFLINE')
    endpoint_url = 'http://localhost:3002/' if offline else None
    return boto3.client('lambda', endpoint_url=endpoint_url)


def dynamo():
    offline = os.getenv('IS_OFFLINE')
    endpoint_url = 'http://localhost:8000/' if offline else None
    dynamodb = boto3.resource('dynamodb', endpoint_url=endpoint_url)
    return dynamodb


def dynamo_client():
    offline = os.getenv('IS_OFFLINE')
    endpoint_url = 'http://localhost:8000/' if offline else None
    client = boto3.client('dynamodb', endpoint_url=endpoint_url)
    return client


def dynamo_table(name):
    return dynamo().Table(name)
