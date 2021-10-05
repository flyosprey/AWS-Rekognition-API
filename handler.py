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


def create_blob(event, context):

    url = create_presigned_url(event["Bucket_key"])

    response = {"statusCode": 200, "body": json.dumps(url)}

    return response
