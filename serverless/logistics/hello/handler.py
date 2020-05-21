import json
import os


def hello(event, context):
    print(os.getenv('IS_OFFLINE'))

    name = json.loads(event["body"]).get("name", "World")
    body = {
        "message": "Hello, {}!".format(name),
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """
