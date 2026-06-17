import json
import boto3
import os

sns = boto3.client('sns')

TOPIC_ARN = os.environ['TOPIC_ARN']

def lambda_handler(event, context):
    message = {
        "status": "SUCCESS",
        "detail": "Lambda executed successfully",
        "event": event
    }

    response = sns.publish(
        TopicArn=TOPIC_ARN,
        Message = f"""
✅ AWS Notification

Status: SUCCESS
Details: Lambda executed successfully

Event Details:
- key1: value1
- key2: value2
- key3: value3
""",
        Subject="AWS Notification"
    )

    return {
        "statusCode": 200,
        "body": json.dumps("Notification sent!")
    }
