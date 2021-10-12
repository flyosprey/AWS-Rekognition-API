import boto3
import json
from constants import DEFAULT_REGION_NAME, TABLE_NAME, REGION_NAME


def get_labels_info(blob_id):
    dynamodb_resource = boto3.resource("dynamodb", region_name=REGION_NAME)
    table = dynamodb_resource.Table(TABLE_NAME)


def make_callback(event, context):
    blob_id = event["pathParameters"]["blob_id"]
