import boto3
import urllib.parse
import json
from constants import BUCKET_NAME, DEFAULT_REGION_NAME


def detect_labels(photo):
    rekognition_client = boto3.client("rekognition", region_name=DEFAULT_REGION_NAME)
    response = rekognition_client.detect_labels(
                                                Image={"S3Object": {"Bucket": BUCKET_NAME, "Name": photo}},
                                                MaxLabels=18
                                                )

    return response


def process_blob(event, context):
    s3 = boto3.client("s3", region_name=DEFAULT_REGION_NAME)
    file_name = urllib.parse.unquote_plus(event["Records"][0]["s3"]["object"]["key"], encoding="utf-8")
    file_object = s3.get_object(Bucket=BUCKET_NAME, Key=file_name)

    return file_object["ContentType"]
