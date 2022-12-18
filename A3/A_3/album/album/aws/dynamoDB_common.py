import logging
from decimal import Decimal

import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
KEY_IMAGE_TABLE = 'key_image'
SHARED_LINK_TABLE = 'shared_link'
STATISTICS_TABLE = 'statistics'

STATISTICS = 'Statistics'
VALUE = 'Value'
CAPACITY = 'Capacity'
IMAGE_NUMBER = 'Total Number of Images'
USER_NUMBER = 'Total Number of active users'
CALL_NUMBER = 'Number of Calls to Lambda Function'


def db_upload_image(key, image, user, last_time_accessed):
    table1 = dynamodb.Table(KEY_IMAGE_TABLE)
    response = table1.put_item(
        Item={
            'Key': key,
            'Image': image,
            'Thumbnail': " ",
            'User': user,
            'Tag': " ",
            'Last time accessed': last_time_accessed
        }
    )
    table2 = dynamodb.Table(SHARED_LINK_TABLE)
    response = table2.put_item(
        Item={
            'Image key': key,
            'Share key': ' ',
            'Number of accesses': 0,
            'Is shared': 'False'
        }
    )
    logging.info('Upload image successfully')


def db_delete_image(key):
    tableName1 = KEY_IMAGE_TABLE
    tableName2 = SHARED_LINK_TABLE
    table1 = dynamodb.Table(tableName1)
    table2 = dynamodb.Table(tableName2)

    response1 = table1.delete_item(
        Key={
            'Key': key
        }
    )
    response2 = table2.delete_item(
        Key={
            'Image key': key
        }
    )


def db_update_access_time(key, last_time_accessed):
    table = dynamodb.Table(KEY_IMAGE_TABLE)

    response = table.update_item(
        Key={'Key': key},
        UpdateExpression="set #Last_time_accessed=:last_time_accessed",
        ExpressionAttributeValues={':last_time_accessed': last_time_accessed},
        ExpressionAttributeNames={'#Last_time_accessed': 'Last time accessed'},
        ReturnValues="UPDATED_NEW")


def db_set_is_shared(key, is_shared):
    tableName = SHARED_LINK_TABLE
    table = dynamodb.Table(tableName)

    response = table.update_item(
        Key={'Image key': key},
        UpdateExpression="set #is_shared=:share",
        ExpressionAttributeValues={
            ':share': is_shared},
        ExpressionAttributeNames={'#is_shared': 'Is shared'},
        ReturnValues="UPDATED_NEW")


def db_get_shared_link_table_attributes(key):
    tableName = SHARED_LINK_TABLE

    table = dynamodb.Table(tableName)
    response = table.get_item(
        Key={
            'Image key': key
        }
    )
    if len(response['Item']) == 0:
        return None
    else:
        records = {}
        records['key'] = key
        records['share_link'] = response['Item'].get('Share key')
        records['number_of_access'] = response['Item'].get('Number of accesses')
        records['is_shared'] = response['Item'].get('Is shared')
        return records


def db_get_stats_from_table(stats_type):
    table = dynamodb.Table(STATISTICS_TABLE)
    item = table.get_item(
        Key={
            STATISTICS: stats_type
        }
    )
    return item['Item'][VALUE]


def update_statistics(stats_type, increase_num):
    table = dynamodb.Table(STATISTICS_TABLE)

    curr_value = db_get_stats_from_table(stats_type)

    response = table.update_item(
        Key={STATISTICS: stats_type},
        UpdateExpression="set #Value=:new",
        ExpressionAttributeValues={
            ':new': curr_value + increase_num},
        ExpressionAttributeNames={'#Value': VALUE},
        ReturnValues="UPDATED_NEW")


def db_get_table_stats():
    table = dynamodb.Table(KEY_IMAGE_TABLE)
    response = table.scan(IndexName='UserIndex')
    users = []
    num = 0
    for item in response['Items']:
        num = num + 1
        if item.get('User') not in users:
            users.append(item.get('User'))

    while 'LastEvaluatedKey' in response:
        response = table.scan(
            IndexName="UserIndex",
            ExclusiveStartKey=response['LastEvaluatedKey']
        )
        for item in response['Items']:
            num = num + 1
            if item.get('User') not in users:
                users.append(item.get('User'))
    result = {}
    result['image_number'] = num
    result['user_number'] = len(users)
    return result

def db_reset_share(key):
    table = dynamodb.Table(SHARED_LINK_TABLE)

    response = table.update_item(
        Key={'Image key': key},
        UpdateExpression="set #Value=:new",
        ExpressionAttributeValues={
            ':new': -1},
        ExpressionAttributeNames={'#Value': 'Number of accesses'},
        ReturnValues="UPDATED_NEW")