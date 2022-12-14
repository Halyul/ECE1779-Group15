# A3_background_update - used for updating some statistics and image processing

## setup process
1. Create function
    1. goto Lambda, click 'Create function'
    2. choose 'Use a blueprint'
    3. use 's3' as filter, then select 'Get S3 object' which uses 'python3.7'
    4. enter the function name (A3_background_update this case)
    5. under 'Role name', type anything (I used ECE1779_A3_background_update_role)
    6. under 'S3 trigger', pick the correct bucket
    7. check the box of 'I acknowledge that using the same S3 bucket for both input and output is not recommended and that this configuration can cause recursive invocations, increased Lambda usage, and increased costs.'
    8. leave the rest as default and click 'Create function'
2. upload function
    1. goto the page of the newly created function
    2. click 'Upload from' choose '.zip file'
    3. click 'Upload', then update the file 'A3_background_update.zip', and click 'save'
    4. should able to see the code on the online IDE
    5. change the 'bucket_name' in 'config.py' to your S3 bucket used in Assignment 3
    6. change the 'api_gateway_url' in 'config.py' to your API Gateway used in Assignment 3 for shared image access
    7. click 'Deploy'
3. set permission
    1. click 'Configuration' on the page
    2. goto 'Permissions' then click the link under the 'Role name' (in the format of <function_name>-role-<something>), another page should pop up
    3. in the new page, click the button 'Add permissions', choose 'Attach policies'
    4. enter 'AmazonS3FullAccess' in the filter, then select it, click 'Attach policies'
    5. click the button 'Add permissions' then choose 'Attach policies' again
    6. enter 'AmazonDynamoDBFullAccess' in the filter, then select it, click 'Attach policies'
    7. you can close this page now
4. set trigger
    1. under the 'Function overview' section, click 'Add trigger'
    2. under 'Select a source', choose 'S3'
    3. pick the correct bucket to be used
    4. check the box of 'I acknowledge that using the same S3 bucket for both input and output is not recommended and that this configuration can cause recursive invocations, increased Lambda usage, and increased costs.'
    5. click 'Add'
5. set enviroment
    1. under 'Runtime settings', click 'Edit'
    2. chagne the 'Runtime' to 'Python 3.8', click 'save'
    3. under the 'Layers', click 'Add a layer'
    4. choose 'Specify an ARN', then type in 'arn:aws:lambda:us-east-1:770693421928:layer:Klayers-p38-Pillow:5', click Verify, then click 'Add'
    5. under the 'Layers', click 'Add a layer' again
    6. choose 'Specify an ARN', then type in 'arn:aws:lambda:us-east-1:770693421928:layer:Klayers-p38-requests:7', click Verify, then click 'Add'
    7. under the 'Layers', click 'Add a layer' again
    8. choose 'Specify an ARN', then type in 'arn:aws:lambda:us-east-1:770693421928:layer:Klayers-p38-pytz:3', click Verify, then click 'Add'

