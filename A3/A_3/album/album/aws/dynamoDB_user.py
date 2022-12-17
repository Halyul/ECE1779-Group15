from __future__ import print_function

import base64

from album.aws.dynamoDB_common import KEY_IMAGE_TABLE, dynamodb, SHARED_LINK_TABLE, db_get_shared_link_table_attributes


def db_get_image_by_key_user(user, key):
    tableName = KEY_IMAGE_TABLE

    table = dynamodb.Table(tableName)
    response = table.get_item(
        Key={
            'Key': key
        }
    )
    if 'Item' not in response or response['Item']['User'] != user:
        return None
    else:
        records = {}
        records['key'] = key
        records['user'] = response['Item'].get('User')
        records['number_of_access'] = db_get_shared_link_table_attributes(key).get('number_of_access')
        records['last_time_accessed'] = response['Item'].get('Last time accessed')
        records['thumbnail'] = response['Item'].get('Thumbnail')
        # thumbnail = response['Item'].get('Thumbnail')
        # records['thumbnail'] = "data:{};base64,".format(thumbnail.mimetype).encode("utf-8") + base64.b64encode(thumbnail.read())
        records['tag'] = response['Item'].get('Tag')
        records['share_link'] = db_get_shared_link_table_attributes(key).get('share_link')
        records['is_shared'] = db_get_shared_link_table_attributes(key).get('is_shared')
        records['image_name'] = response['Item'].get('Image')
        return records


def db_get_all_images_user(user):
    tableName = KEY_IMAGE_TABLE

    table = dynamodb.Table(tableName)
    response = table.scan(IndexName='UserIndex')
    records = []
    for item in response['Items']:
        if item.get('User') == user:
            record = {}
            record['key'] = item.get('Key')
            record['user'] = item.get('User')
            record['number_of_access'] = db_get_shared_link_table_attributes(item.get('Key')).get('number_of_access')
            record['last_time_accessed'] = item.get('Last time accessed')
            record['thumbnail'] = response['Item'].get('Thumbnail')
            # thumbnail = response['Item'].get('Thumbnail')
            # record['thumbnail'] = "data:{};base64,".format(thumbnail.mimetype).encode("utf-8") + base64.b64encode(
            #     thumbnail.read())
            record['tag'] = item.get('Tag')
            record['share_link'] = db_get_shared_link_table_attributes(item.get('Key')).get('share_link')
            record['is_shared'] = db_get_shared_link_table_attributes(item.get('Key')).get('is_shared')
            record['image_name'] = item.get('Image')
            records.append(record)

    while 'LastEvaluatedKey' in response:
        response = table.scan(
            IndexName="UserIndex",
            ExclusiveStartKey=response['LastEvaluatedKey']
        )
        for item in response['Items']:
            if item.get('User') == user:
                record = {}
                record['key'] = item.get('Key')
                record['user'] = item.get('User')
                record['number_of_access'] = db_get_shared_link_table_attributes(item.get('Key')).get(
                    'number_of_access')
                record['last_time_accessed'] = item.get('Last time accessed')
                record['thumbnail'] = response['Item'].get('Thumbnail')
                # thumbnail = response['Item'].get('Thumbnail')
                # record['thumbnail'] = "data:{};base64,".format(thumbnail.mimetype).encode("utf-8") + base64.b64encode(
                #     thumbnail.read())
                record['tag'] = item.get('Tag')
                record['share_link'] = db_get_shared_link_table_attributes(item.get('Key')).get('share_link')
                record['is_shared'] = db_get_shared_link_table_attributes(item.get('Key')).get('is_shared')
                record['image_name'] = item.get('Image')
                records.append(record)
    return records


def db_is_allowed_get_shared_image(key):
    tableName = SHARED_LINK_TABLE

    table = dynamodb.Table(tableName)
    response = table.get_item(
        Key={
            'Image key': key
        }
    )
    if 'Item' not in response or response['Item']['Is shared'] != 'True':
        return False
    else:
        return True
