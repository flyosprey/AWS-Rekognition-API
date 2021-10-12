import boto3
import urllib.parse
import json
from decimal import Decimal
from botocore.exceptions import ClientError
from constants import BUCKET_NAME, TABLE_NAME, REGION_NAME


def detect_photo_labels(s3_blob_key):
    try:
        rekognition_client = boto3.client("rekognition", region_name=REGION_NAME)
        labels = rekognition_client.detect_labels(
            Image={"S3Object": {"Bucket": BUCKET_NAME, "Name": s3_blob_key}},
            MaxLabels=10
        )
    except ClientError as e:
        print(e.response["Error"]["Message"])
    else:
        for label in labels["Labels"]:
            del label["Instances"]
        labels = json.loads(json.dumps(labels["Labels"]), parse_float=Decimal)

        return labels


def put_labels_info(labels, dynamodb_blob_id):
    dynamodb_client = boto3.resource("dynamodb", region_name=REGION_NAME)
    table = dynamodb_client.Table(TABLE_NAME)
    try:
        dynamodb_response = table.update_item(
            Key={
                'blob_id': dynamodb_blob_id,
            },
            UpdateExpression="set labels_photo=:l",
            ExpressionAttributeValues={
                ':l': labels
            },
            ReturnValues="UPDATED_NEW"
        )
    except ClientError as e:
        print(e.response["Error"]["Message"])
    else:
        return dynamodb_response


def process_blob(event, context):
    s3_blob_key = urllib.parse.unquote_plus(event["Records"][0]["s3"]["object"]["key"], encoding="utf-8")
    dynamodb_blob_id = s3_blob_key.replace(".png", "")
    labels = detect_photo_labels(s3_blob_key)
    response = put_labels_info(labels, dynamodb_blob_id)

    return response
