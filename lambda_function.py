import json
import urllib.parse

def lambda_handler(event, context):

    #  Handle S3 event (new feature)
    if 'Records' in event:
        for record in event['Records']:
            bucket = record['s3']['bucket']['name']
            key = urllib.parse.unquote_plus(record['s3']['object']['key'])
            event_time = record['eventTime']

            print("S3 Upload Detected ")
            print(f"Bucket: {bucket}")
            print(f"File: {key}")
            print(f"Upload Time: {event_time}")

    #  Existing logic (your original demo)
    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Hello Wissen! Existing functionality works, verified "})
    }
