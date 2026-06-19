import json
import boto3
from PIL import Image
import io
from datetime import datetime

s3 = boto3.client('s3')
sns = boto3.client('sns')

# ✅ DESTINATION BUCKET
DEST_BUCKET = "processed-image-buckt"

# ✅ SNS Topic ARN
SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:447580526006:sns-wissen"

def lambda_handler(event, context):

    # ✅ Get input details
    bucket = event.get('bucket')
    key = event.get('key')

    if not bucket or not key:
        return {
            "statusCode": 400,
            "body": "Invalid input event"
        }

    print(f"Processing file: {key} from source bucket: {bucket}")

    # ✅ Step 1: Get image from source bucket
    response = s3.get_object(Bucket=bucket, Key=key)
    image_data = response['Body'].read()

    # ✅ Step 2: Open image using Pillow
    image = Image.open(io.BytesIO(image_data))

    # ✅ Step 3: Resize image
    image = image.resize((800, 800))

    # ✅ Step 4: Save processed image to memory
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG", quality=70)
    buffer.seek(0)

    # ✅ Step 5: New filename
    new_key = f"processed-{key}"

    # ✅ Step 6: Upload to processed bucket
    s3.put_object(
        Bucket=DEST_BUCKET,
        Key=new_key,
        Body=buffer,
        ContentType="image/jpeg"
    )

    print(f"✅ Processed file uploaded to {DEST_BUCKET}/{new_key}")

    # ✅ Step 7: Calculate processed file size
    file_size_kb = round(len(buffer.getvalue()) / 1024, 2)

    # ✅ Step 8: Timestamp
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    # ✅ Step 9: SNS Notification
    message = f"""
✅ Image Processing Complete

Processed File Name: {new_key}
Processed File Size: {file_size_kb} KB
Bucket Name: {DEST_BUCKET}
Timestamp: {timestamp}
    print("✅ SNS notification sent")

    return {
        "body": "Image processed and notification sent ✅"
    }        "statusCode": 200,

The processed image is now available for download ✅
"""

    sns.publish(
    )

        Message=message

