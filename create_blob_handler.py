import json
import uuid
import boto3
import urllib.request
import urllib.error
from botocore.exceptions import ClientError
from botocore.config import Config
from constants import REGION_NAME, BUCKET_NAME, TABLE_NAME


def create_presigned_url(blob_key):
    s3_client = boto3.client("s3", config=Config(signature_version="s3v4"), region_name=REGION_NAME)
    try:
        url = s3_client.generate_presigned_url(
            "put_object",
            Params={"Bucket": BUCKET_NAME, "Key": blob_key},
            HttpMethod="PUT",
            ExpiresIn=3600
        )
    except ClientError as e:
        print(e.response["Error"]["Message"])
    else:
        return url


def put_item_dynamodb(callback_url, blob_id):
    try:
        dynamodb_resource = boto3.resource("dynamodb", region_name=REGION_NAME)
        table = dynamodb_resource.Table(TABLE_NAME)
        items = {"blob_id": blob_id, "callback_url": callback_url}
        table.put_item(Item=items)
    except ClientError as e:
        print(e.response["Error"]["Message"])


def is_url(url):
    try:
        urllib.request.urlopen(url)
    except urllib.error.URLError or urllib.error.HTTPError:
        return False
    else:
        return True


def create_blob(event, context):
    blob_id = str(uuid.uuid4())
    bucket_key = blob_id + ".png"
    sent_items = json.loads(event["body"])
    callback_url = sent_items["callback_url"]
    if is_url(callback_url):
        url = create_presigned_url(bucket_key)
        put_item_dynamodb(callback_url, blob_id)
        response = {
            "url": url,
            "blob_id": blob_id,
            "callback_url": callback_url
        }
    else:
        return {"statusCode": 400, "body": json.dumps("Invalid callback url supplied")}

    return {"statusCode": 200, "body": json.dumps(response)}
