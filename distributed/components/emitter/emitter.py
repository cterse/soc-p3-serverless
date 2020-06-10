import json
import logging
import requests
import boto3

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)
logger = logging.getLogger('pos')

client = boto3.client('lambda')


def lambda_handler(event, context):
    # TODO implement
    print(str(event))
    print("Parameters are " + str(event["parameters"]))
    print(event["parameters"])
    message = event["parameters"]
    message = str(message)
    message = message.replace("\'", "\"")
    message = json.loads(message)
    print(message)
    response = requests.post(event["to"], json=message)
    print(str(response.text))
    return {
        'statusCode': 200,
        'body': json.dumps('Message has been sent!')
    }
