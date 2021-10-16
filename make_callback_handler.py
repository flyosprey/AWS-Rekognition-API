import boto3
import urllib3
import json
from botocore.exceptions import ClientError
from constants import REGION_NAME, TABLE_NAME, REGION_NAME


def get_labels_info(blob_id):
    dynamodb_resource = boto3.resource("dynamodb", region_name=REGION_NAME)
    table = dynamodb_resource.Table(TABLE_NAME)
    try:
        response = table.get_item(Key={"blob_id": blob_id})
    except ClientError as e:
        print(e.response["Error"]["Message"])
    else:
        return response


def make_callback(event, context):
    http = urllib3.PoolManager()
    blob_id = event["pathParameters"]["blob_id"]
    dynamodb_response = get_labels_info(blob_id)
    if "Item" not in dynamodb_response.keys():
        error_404 = {"message": "Blob not found"}
        return {"statusCode": 404, "body": json.dumps(error_404)}
    else:
        callback_url = dynamodb_response["Item"]["callback_url"]
        labels_info = json.dumps(dynamodb_response["Item"]["labels_photo"], ensure_ascii=False, default=str)
        callback_response = http.request(
            "POST",
            callback_url,
            body=labels_info,
            headers={"Content-Type": "application/json"}
        )
    if callback_response.status != 200:
        error = {"message": "Problem with your callback url"}
        return {"statusCode": callback_response.status, "body": json.dumps(error)}
    else:
        response = {"callback_url": callback_url, "labels": labels_info}
        return {"statusCode": 200, "body": json.dumps(response)}
