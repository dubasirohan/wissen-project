import json
import urllib.parse
import boto3

sns = boto3.client('sns')
s3 = boto3.client('s3')

SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:447580526006:sns-wissen"

def is_valid_image(key):
    return key.lower().endswith(('.jpg', '.png'))

def lambda_handler(event, context):

    if 'Records' in event:
        for record in event['Records']:
            bucket = record['s3']['bucket']['name']
            key = urllib.parse.unquote_plus(record['s3']['object']['key'])
            event_time = record['eventTime']

            print("S3 Upload Detected")
            print(f"Bucket: {bucket}")
            print(f"File: {key}")
            print(f"Upload Time: {event_time}")

            # ✅ VALID IMAGE CASE
            if is_valid_image(key):
                message = f"""
✅ Upload Successful

Bucket Name: {bucket}
File Name: {key}
Timestamp: {event_time}
"""

                sns.publish(
                    TopicArn="arn:aws:sns:us-east-1:447580526006:sns-wissen",
                    Subject="Image Upload Success",
                    Message=message
                )

            # ❌ INVALID FILE CASE
            else:
                # delete file
                s3.delete_object(Bucket=bucket, Key=key)

                message = f"""
❌ Upload Failed

Reason: File is not a supported image type (.jpg / .png)

Bucket Name: {bucket}
File Name: {key}
Timestamp: {event_time}
"""

                sns.publish(
                    TopicArn="arn:aws:sns:us-east-1:447580526006:sns-wissen",
                    Subject="Upload Failed - Invalid File",
                    Message=message
                )

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Validation complete, successful, process now"})
    }
