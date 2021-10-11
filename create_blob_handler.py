import json
import uuid
import boto3
import logging
from botocore.exceptions import ClientError
from botocore.config import Config
from constants import DEFAULT_REGION_NAME, BUCKET_NAME


def create_presigned_url(bucket_key):
    s3_client = boto3.client("s3", config=Config(signature_version="s3v4"), region_name=DEFAULT_REGION_NAME)
    try:
        url = s3_client.generate_presigned_url("put_object",
                                               Params={"Bucket": BUCKET_NAME, "Key": bucket_key},
                                               HttpMethod="PUT",
                                               ExpiresIn=3600)
    except ClientError as e:
        logging.error(e)
        return None

    return url


def put_item_dynamodb(callback_url, blob_id):
    client = boto3.resource("dynamodb", region_name=DEFAULT_REGION_NAME)
    table = client.Table("Blobs")
    items = {"blob_id": blob_id, "callback_url": callback_url}
    response = table.put_item(Item=items)

    return response


def create_blob(event, context):
    blob_id = str(uuid.uuid4())
    callback_url = event["callback_url"]
    url = create_presigned_url(event["bucket_key"])
    db_response = put_item_dynamodb(callback_url, blob_id)
    response = {"status_code": 200, "url": json.dumps(db_response), "blob_id": json.dumps(blob_id)}

    return response
