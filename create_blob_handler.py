import json
import uuid
import boto3
import logging
from botocore.exceptions import ClientError
from botocore.config import Config
from constants import DEFAULT_REGION_NAME, BUCKET_NAME


def create_presigned_url(bucket_key, expiration=5*60):
    s3_client = boto3.client("s3", config=Config(signature_version="s3v4"),
                             region_name=DEFAULT_REGION_NAME)

    try:
        url = s3_client.generate_presigned_url("put_object",
                                               Params={"Bucket": BUCKET_NAME,
                                                       "Key": bucket_key
                                                       },
                                               HttpMethod="PUT",
                                               ExpiresIn=expiration)

    except ClientError as e:
        logging.error(e)
        return None

    return url


def put_item_dynamodb(callback_url):
    blob_id = str(uuid.uuid4())

    client = boto3.resource("dynamodb", region_name=DEFAULT_REGION_NAME)
    table = client.Table("Blobs")

    items = {"blob_id": blob_id, "callback_url": callback_url}

    response = table.put_item(Item=items)

    return response


def create_blob(event, context):

    callback_url = event["Callback_url"]
    url = create_presigned_url(event["Bucket_key"])

    db_responce = put_item_dynamodb(callback_url)

    response = {"statusCode": 200, "body": json.dumps(db_responce)}

    return response
