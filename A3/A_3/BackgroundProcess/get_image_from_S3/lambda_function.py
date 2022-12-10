import json
import urllib.parse
import boto3
from collections.abc import Mapping
import base64

from dynamodb_func import update_shared_link_number_of_accesses, update_num_calls_statistics

print('Loading function')

bucket_name = '1779-week-6-exercises-bucket'

def lambda_handler(event, context):
    try:
        if 'queryStringParameters' in event and event['queryStringParameters'] != None:
            event = event["queryStringParameters"]
        else:
            if isinstance(event["body"], Mapping):
                event = event["body"]
            else:
                event = json.loads(event["body"])
    except Exception as e:
        return "Error: {}".format(e)

    # Get the object from the event and show its content type
    print("event = {}".format(event))
    key = event['key'] # key is the name of the image
    print("Got key = {}".format(key))
    s3 = boto3.client("s3")
    try:
        response = s3.get_object(Bucket=bucket_name, Key=key)
        file_data = response["Body"].read()
        
        # update dynamo db info
        update_shared_link_number_of_accesses(key)
        update_num_calls_statistics()
        
        return {
            'statusCode': 200,
            'body': base64.b64encode(file_data),
            'headers': {'Content-Type' : 'image/jpg'},
            'isBase64Encoded': True
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps('Error! {}'.format(e))
        }