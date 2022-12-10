import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

def get_item_from_table(table_name, index_name, index_value):
    table = dynamodb.Table(table_name)
    item = table.get_item(Key={index_name: index_value})
    return item['Item']
    
def update_shared_link_number_of_accesses(new_image):
    # update the 'Number of accesses' in dynamo db
    tableName = 'shared_link'
    table = dynamodb.Table(tableName)
    # get num_of_access
    curr_num_of_access = get_item_from_table('shared_link', 'Image key', new_image)['Number of accesses']
    curr_num_of_access = int(curr_num_of_access)
    
    response = table.update_item(
        Key={'Image key': new_image},
        UpdateExpression="set #Number_of_accesses=:access",
        ExpressionAttributeValues={
            ':access': curr_num_of_access+1},
        ExpressionAttributeNames={'#Number_of_accesses': 'Number of accesses'},
        ReturnValues="UPDATED_NEW")
        
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