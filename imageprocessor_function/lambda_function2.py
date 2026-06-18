import json
import boto3
from PIL import Image
import io

s3 = boto3.client('s3')

DEST_BUCKET = "processed-image-bucket"

def lambda_handler(event, context):

    bucket = event['bucket']
    key = event['key']

    print(f"Processing file: {key} from bucket: {bucket}")

    # Get image from upload bucket
    response = s3.get_object(Bucket=bucket, Key=key)
    image_data = response['Body'].read()

    # Open image
    image = Image.open(io.BytesIO(image_data))

    # ✅ Resize (you can change dimensions)
    image = image.resize((800, 800))

    # ✅ Compress + convert format
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG", quality=70)
    buffer.seek(0)

    # Save to processed bucket
    new_key = f"processed-{key}"

    s3.put_object(
        Bucket=DEST_BUCKET,
        Key=new_key,
        Body=buffer,
        ContentType="image/jpeg"
    )

    print(f"✅ Processed image saved: {new_key}")

    return {
        "statusCode": 200,
        "body": json.dumps("Image processed successfully")
    }