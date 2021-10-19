import boto3
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
    blob_id = event["pathParameters"]["blob_id"]
    dynamodb_response = get_labels_info(blob_id)
    if "Item" not in dynamodb_response.keys():
        error_404 = {"message": "Blob not found"}
        return {"statusCode": 404, "body": json.dumps(error_404)}
    else:
        labels_info = json.loads(json.dumps(dynamodb_response["Item"]["labels_photo"], default=float))
        print(type(labels_info))
        print(labels_info[0]["Confidence"])
        response = {"labels": labels_info}
        return {"statusCode": 200, "body": json.dumps(response)}
