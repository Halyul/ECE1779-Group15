import logging

import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
KEY_IMAGE_TABLE = 'key_image'
SHARED_LINK_TABLE = 'shared_link'
STATISTICS_TABLE = 'statistics'


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
            'Is shared': 'false'
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


def db_get_item_from_table(table_name, index_name, index_value):
    table = dynamodb.Table(table_name)
    item = table.get_item(Key={index_name: index_value})
    return item['Item']


def update_num_calls_statistics():
    tableName = 'statistics'
    table = dynamodb.Table(tableName)

    # get current num_calls
    curr_num_of_call = db_get_item_from_table('statistics', 'Statistics', 'Number of Calls to Lambda Function')['Value']
    curr_num_of_call = int(curr_num_of_call)

    response = table.update_item(
        Key={'Statistics': 'Number of Calls to Lambda Function'},
        UpdateExpression="set #Value=:calls",
        ExpressionAttributeValues={
            ':calls': curr_num_of_call + 1},
        ExpressionAttributeNames={'#Value': 'Value'},
        ReturnValues="UPDATED_NEW")