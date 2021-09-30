import json
import uuid
import boto3
import logging
from botocore.exceptions import ClientError
from .constants import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, DEFAULT_REGION_NAME


def create_presigned_url(event, expiration=5*60):
    s3_client = boto3.client("s3", region_name=DEFAULT_REGION_NAME,
                             aws_access_key_id=AWS_ACCESS_KEY_ID,
                             aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    try:
        url = s3_client.generate_presigned_url("put_object",
                                               Params={"Bucket": event["Bucket_name"],
                                                       "Key": event["Bucket_key"]
                                                       },
                                               HttpMethod="PUT",
                                               ExpiresIn=expiration)

    except ClientError as e:
        logging.error(e)
        return None

    return url


def create_blob(event, context):

    url = create_presigned_url(event)

    response = {"statusCode": 200, "body": json.dumps(url)}

    return response

