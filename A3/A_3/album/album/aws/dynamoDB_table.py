import boto3

from album.aws.dynamoDB_common import dynamodb, SHARED_LINK_TABLE, KEY_IMAGE_TABLE, STATISTICS_TABLE, STATISTICS, VALUE, \
    CAPACITY, IMAGE_NUMBER, USER_NUMBER, CALL_NUMBER


def db_create_table_shared():
    table = dynamodb.create_table(
        TableName=SHARED_LINK_TABLE,
        KeySchema=[
            {
                'AttributeName': 'Image key',
                'KeyType': 'HASH'  # Partition key
            },
        ],
        GlobalSecondaryIndexes=[
            {
                'IndexName': "ShareKeyIndex",
                'KeySchema': [
                    {
                        'KeyType': 'HASH',
                        'AttributeName': 'Share key'
                    },
                    {
                        'KeyType': 'RANGE',
                        'AttributeName': 'Image key'
                    }
                ],
                'Projection': {
                    'ProjectionType': 'ALL',
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 2,
                    'WriteCapacityUnits': 2
                }
            },
            {
                'IndexName': "NumberOfAccessesIndex",
                'KeySchema': [
                    {
                        'KeyType': 'HASH',
                        'AttributeName': 'Number of accesses'
                    },
                    {
                        'KeyType': 'RANGE',
                        'AttributeName': 'Image key'
                    }
                ],
                'Projection': {
                    'ProjectionType': 'ALL',
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 2,
                    'WriteCapacityUnits': 2
                }
            },
            {
                'IndexName': "IsSharedIndex",
                'KeySchema': [
                    {
                        'KeyType': 'HASH',
                        'AttributeName': 'Is shared'
                    },
                    {
                        'KeyType': 'RANGE',
                        'AttributeName': 'Image key'
                    }
                ],
                'Projection': {
                    'ProjectionType': 'ALL',
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 2,
                    'WriteCapacityUnits': 2
                }
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'Image key',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'Share key',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'Number of accesses',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'Is shared',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )


def db_create_table_key_image():
    table = dynamodb.create_table(
        TableName=KEY_IMAGE_TABLE,
        KeySchema=[
            {
                'AttributeName': 'Key',
                'KeyType': 'HASH'  # Partition key
            },
        ],
        GlobalSecondaryIndexes=[
            {
                'IndexName': "UserIndex",
                'KeySchema': [
                    {
                        'KeyType': 'HASH',
                        'AttributeName': 'User'
                    },
                    {
                        'KeyType': 'RANGE',
                        'AttributeName': 'Key'
                    }
                ],
                'Projection': {
                    'ProjectionType': 'ALL',
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 2,
                    'WriteCapacityUnits': 2
                }
            },
            {
                'IndexName': "TagIndex",
                'KeySchema': [
                    {
                        'KeyType': 'HASH',
                        'AttributeName': 'Tag'
                    },
                    {
                        'KeyType': 'RANGE',
                        'AttributeName': 'Key'
                    }
                ],
                'Projection': {
                    'ProjectionType': 'ALL',
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 2,
                    'WriteCapacityUnits': 2
                }
            },
            {
                'IndexName': "ImageIndex",
                'KeySchema': [
                    {
                        'KeyType': 'HASH',
                        'AttributeName': 'Image'
                    },
                    {
                        'KeyType': 'RANGE',
                        'AttributeName': 'Key'
                    }
                ],
                'Projection': {
                    'ProjectionType': 'ALL',
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 2,
                    'WriteCapacityUnits': 2
                }
            },
            {
                'IndexName': "ThumbnailIndex",
                'KeySchema': [
                    {
                        'KeyType': 'HASH',
                        'AttributeName': 'Thumbnail'
                    },
                    {
                        'KeyType': 'RANGE',
                        'AttributeName': 'Key'
                    }
                ],
                'Projection': {
                    'ProjectionType': 'ALL',
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 2,
                    'WriteCapacityUnits': 2
                }
            },
            {
                'IndexName': "AccessTimeIndex",
                'KeySchema': [
                    {
                        'KeyType': 'HASH',
                        'AttributeName': 'Last time accessed'
                    },
                    {
                        'KeyType': 'RANGE',
                        'AttributeName': 'Key'
                    }
                ],
                'Projection': {
                    'ProjectionType': 'ALL',
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 2,
                    'WriteCapacityUnits': 2
                }
            }

        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'Key',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'Image',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'Thumbnail',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'User',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'Tag',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'Last time accessed',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )


def db_create_table_stats():
    table = dynamodb.create_table(
        TableName=STATISTICS_TABLE,
        KeySchema=[
            {
                'AttributeName': STATISTICS,
                'KeyType': 'HASH'  # Partition key
            }
        ],
        GlobalSecondaryIndexes=[
            {
                'IndexName': "ValueIndex",
                'KeySchema': [
                    {
                        'KeyType': 'HASH',
                        'AttributeName': 'Value'
                    },
                    {
                        'KeyType': 'RANGE',
                        'AttributeName': 'Statistics'
                    }
                ],
                'Projection': {
                    'ProjectionType': 'ALL',
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 2,
                    'WriteCapacityUnits': 2
                }
            }
        ],

        AttributeDefinitions=[
            {
                'AttributeName': STATISTICS,
                'AttributeType': 'S'
            },
            {
                'AttributeName': VALUE,
                'AttributeType': 'N'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )


def db_delete_table(table_name):
    dynamodb = boto3.client('dynamodb', region_name='us-east-1')

    response = dynamodb.delete_table(
        TableName=table_name
    )


def db_intiate_stats_table():
    table = dynamodb.Table(STATISTICS_TABLE)
    table.put_item(
        Item={
            STATISTICS: CAPACITY,
            VALUE: 0
        }
    )
    table.put_item(
        Item={
            STATISTICS: IMAGE_NUMBER,
            VALUE: 0
        }
    )
    table.put_item(
        Item={
            STATISTICS: USER_NUMBER,
            VALUE: 0
        }
    )
    table.put_item(
        Item={
            STATISTICS: CALL_NUMBER,
            VALUE: 0
        }
    )
