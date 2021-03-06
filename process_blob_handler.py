import boto3
import urllib.parse
import urllib3
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
        return labels


def put_labels_info(labels, dynamodb_blob_id):
    labels = json.loads(json.dumps(labels["Labels"]), parse_float=Decimal)
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


def get_callback_url(blob_id):
    dynamodb_client = boto3.resource("dynamodb", region_name=REGION_NAME)
    table = dynamodb_client.Table(TABLE_NAME)
    try:
        items = table.get_item(Key={"blob_id": blob_id})
        callback_url = items["Item"]["callback_url"]
    except ClientError as e:
        print(e.response["Error"]["Message"])
    else:
        return callback_url


def send_callback(callback_url, labels):
    labels = json.loads(json.dumps(labels["Labels"], default=float))
    http = urllib3.PoolManager()
    callback_response = http.request(
            "POST",
            callback_url,
            body=json.dumps(labels),
            headers={"Content-Type": "application/json"})
    
    return callback_response


def process_blob(event, context):
    blob_id = urllib.parse.unquote_plus(event["Records"][0]["s3"]["object"]["key"], encoding="utf-8")
    callback_url = get_callback_url(blob_id)
    labels = detect_photo_labels(blob_id)
    send_callback(callback_url, labels)
    put_labels_info_response = put_labels_info(labels, blob_id)

    return put_labels_info_response
