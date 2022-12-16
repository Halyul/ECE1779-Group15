from album.aws.dynamoDB_common import SHARED_LINK_TABLE, dynamodb, KEY_IMAGE_TABLE


def db_set_tag(key, tag):
    tableName = KEY_IMAGE_TABLE
    table = dynamodb.Table(tableName)

    response = table.update_item(
        Key={'Key': key},
        UpdateExpression="set #tag=:tag",
        ExpressionAttributeValues={
            ':tag': tag},
        ExpressionAttributeNames={'#tag': 'Tag'},
        ReturnValues="UPDATED_NEW")


def db_set_thumbnail(key, thumbnail):
    tableName = KEY_IMAGE_TABLE
    table = dynamodb.Table(tableName)

    response = table.update_item(
        Key={'Key': key},
        UpdateExpression="set #thumbnail=:thumbnail",
        ExpressionAttributeValues={
            ':thumbnail': thumbnail},
        ExpressionAttributeNames={'#thumbnail': 'Thumbnail'},
        ReturnValues="UPDATED_NEW")