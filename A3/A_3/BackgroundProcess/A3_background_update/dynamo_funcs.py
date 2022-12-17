import boto3
from boto3.dynamodb.conditions import Key
from datetime import datetime
from pytz import timezone

import config

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

def get_new_key_from_image(new_image):
    tableName = 'key_image'
    indexName = 'ImageIndex'

    table = dynamodb.Table(tableName)
    response = table.scan(IndexName=indexName)
    records = []
    for i in response['Items']:
        records.append(i)
    while 'LastEvaluatedKey' in response:
        response = table.scan(
            IndexName=indexName,
            ExclusiveStartKey=response['LastEvaluatedKey']
        )
        for i in response['Items']:
            records.append(i)

    for item in records:
        if item['Image'] == new_image:
            return item['Key']
    print("Error - Image {} is not found on the table!".format(new_image))
    return -1

def set_key_image_table(new_key, new_image, thumbnail_name, new_tag):
    curr_time = datetime.now(timezone('US/Eastern')).strftime("%d/%m/%Y %H:%M:%S")
    
    tableName = 'key_image'
    table = dynamodb.Table(tableName)

    response = table.update_item(
        Key={'Key': new_key},
        UpdateExpression="set Tag=:tag, Thumbnail=:thumbnail, #access_time=:time",
        ExpressionAttributeValues={
            ':tag': new_tag, ':thumbnail': thumbnail_name, ':time': curr_time},
        ExpressionAttributeNames={'#access_time': 'Last time accessed'},
        ReturnValues="UPDATED_NEW")

def set_shared_link_table(new_image):
    tableName = 'shared_link'
    table = dynamodb.Table(tableName)

    shared_url = config.api_gateway_url + config.bucket_name + '?key=' + new_image

    response = table.update_item(
        Key={'Image key': new_image},
        UpdateExpression="set #Share_key=:share",
        ExpressionAttributeValues={
            ':share': shared_url},
        ExpressionAttributeNames={'#Share_key': 'Share key'},
        ReturnValues="UPDATED_NEW")

def get_item_from_table(table_name, index_name, index_value):
    table = dynamodb.Table(table_name)
    item = table.get_item(Key={index_name: index_value})
    return item['Item']

def update_num_calls_statistics():
    tableName = 'statistics'
    table = dynamodb.Table(tableName)
    
    # get current num_calls
    curr_num_of_call = get_item_from_table('statistics', 'Statistics', 'Number of Calls to Lambda Function')['Value']
    curr_num_of_call = int(curr_num_of_call)
    
    response = table.update_item(
        Key={'Statistics': 'Number of Calls to Lambda Function'},
        UpdateExpression="set #Value=:calls",
        ExpressionAttributeValues={
            ':calls': curr_num_of_call+1},
        ExpressionAttributeNames={'#Value': 'Value'},
        ReturnValues="UPDATED_NEW")