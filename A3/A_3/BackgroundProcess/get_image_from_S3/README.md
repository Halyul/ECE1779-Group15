# get_image_from_S3 - used for displaying shared image

# setup process
1. Create function
    1. goto Lambda, click 'Create function'
    2. choose 'Author from scratch'
    3. enter the function name (get_image_from_S3 this case), and choose 'Python 3.9' as the Runtime
    4. leave the rest as default and click 'Create function'
2. upload function
    1. goto the page of the newly created function
    2. click 'Upload from' choose '.zip file'
    3. click 'Upload', then update the file 'get_image_from_S3.zip', and click 'save'
    4. should able to see the code on the online IDE
    5. change the 'bucket_name' in 'lambda_function.py' to your S3 bucket used in Assignment 3
    6. click 'Deploy'
3. set permission
    1. click 'Configuration' on the page
    2. goto 'Permissions' then click the link under the 'Role name' (in the format of <function_name>-role-<something>), another page should pop up
    3. in the new page, click the button 'Add permissions', choose 'Attach policies'
    4. enter 'AmazonS3FullAccess' in the filter, then select it, click 'Attach policies'
    5. click the button 'Add permissions' then choose 'Attach policies' again
    6. enter 'AmazonDynamoDBFullAccess' in the filter, then select it, click 'Attach policies'
    7. you can close this page now
4. set API Gateway
    1. under the 'Function overview' section, click 'Add trigger'
    2. under 'Select a source', choose 'API Gateway'
    3. choose 'Create a new API', select 'REST API' as API type, choose 'Open' under Security, then click 'Add'
    4. goto the link to this API Gateway
    5. goto 'Resources' on the left menu, select '/<function_name>' on the Resources, click 'Actions', click 'Delete Resource', then comfirm 'Delete'
    6. click 'Actions' again, choose 'Create Resource'
          1. use 'bucket' for Resource Name, and '{bucket}' for Resource Path
          2. click 'Create Resource'
    7. click 'Actions' again, choose 'Create Method', then choose 'GET'
          1. choose 'Lambda Function' for Integration type
          2. selete 'Use Lambda Proxy integration'
          3. type in the function name of the newly created lambda function (get_image_from_S3 this case)
          4. click 'save', then 'OK'
          5. choose the 'GET' method, click 'Method Request'
          6. choose 'Validate query string parameters and headers' for 'Request Validator', then click the little tick
          7. goto 'URL Query String Parameters', click 'Add query string'
          8. type in 'key', then click the little tick, choose 'Required' for it
    8. goto 'Settings' on the left menu
          1. in the button, click 'Add Binary Media Type'
          2. type in `*/*`, then click 'Save Changes'
    9. goto 'Resources' on the left menu, click 'Actions' again, choose 'Deploy API'
          1. choose '[New Stage]' for Deployment stage, use anything for the Stage name (I used 'dev')
          2. click Deploy
          3. click on the 'default' stage, then click 'Delete Stage', click 'Delete'
          4. expand the newly created stage, goto the level of 'GET'
          5. there should be an 'Invoke URL' at the top 
          6. replace '{bucket}' with anything, then add '?key=<file_name>' should allow you access images from target S3 bucket
              1. for example, 'https://<something>.execute-api.us-east-1.amazonaws.com/dev/{bucket}' changed to 'https://<something>.execute-api.us-east-1.amazonaws.com/dev/bucket?key=image1.png'
