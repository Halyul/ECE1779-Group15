# AWS Cognito Setup
1. Create a user pool at [here](https://console.aws.amazon.com/cognito/v2/home)
2. At the setup page:
    1. Select `Email` and `User name` under `Cognito user pool sign-in options`
    2. Select `Allow users to sign in with a preferred user name` under `User name requirements`
    3. Select `Next`
    4. Select `No MFA` in `Multi-factor authentication`
    5. Select `Next`
    6. Select `Next`
    7. Select `Send email with Cognito` in `Email`
    8. Select `Next`
    9. Enter a pool name (eg. `1779test`) in `User pool name`
    10. Enter an `App client name` (eg. `react`) in `Initial app client`
    11. Select `Don't generate a client secret`
    12. Select `Next`
    13. Select `Create User Pool`
3. Go to the User Pool details page:
    1. Note down `ARN` under `User pool overview` (eg. `arn:aws:cognito-idp:us-east-1:798322192635:userpool/us-east-1_Wx2PoWcxK`)
    2. Select `Groups` tab
        1. Select `Create group`
        2. Enter a group name of `user`
        3. Select `Create group`
        4. Select `Create group` again
        5. Enter a group name of `admin`
        6. Select `Create group`
4. Create a Lambda function at [here](https://console.aws.amazon.com/lambda/home#/functions)
5. At the setup page:
    1. Select `Author from scratch`
    2. Enter a Function name (eg. `cognitoAddUserToDefaultGroup`) in `Basic information`
    3. Select `Node.js 18.x`
    4. Select `Create function`
6. At the coding page:
    1. Copy and replace the code in the file `index.js` to `index.mjs` in the function editor
    2. Select `Edit` under `Runtime settings`
        1. Change the Handler from `index.handler` to `index.main`
        2. Select `Save`
    3. Select `Deploy`
    4. Select `Configuration` Tab
    5. Select `Permission` Tab
    6. Open the link under `Execution role` (eg. `https://us-east-1.console.aws.amazon.com/iam/home?region=us-east-1#/roles/cognitoAddUserToDefaultGroup-role-qyacm9jv?section=permissions`)
    7. Select `Add permissions` -> `Create inline policy` under `Permissions`
    8. Select `Cognito User Pools` under `Service`
    9. Open `Write` dropdown, select `AdminAddUserToGroup`
    10. Select `Add ARN` under `Resources`
    11. Enter the `ARN` noted down in Step 3 (eg. `arn:aws:cognito-idp:us-east-1:798322192635:userpool/us-east-1_OTyxlD7gH`)
    12. Select `Add`
    13. Select `Review policy`
    14. Enter a `Name` (eg. `cognitoAddUserToGroup`)
    15. Select `Create policy`
7. Go back to User Pool page:
    1. Select `User pool properties` tab
    2. Select `Add Lambda trigger`
    3. Select `Sign-up` under `Lambda triggers`
    4. Select `Post confirmation trigger` under `Lambda triggers`
    5. Select the Lambda function just create (eg. `cognitoAddUserToDefaultGroup`) under `Lambda function`
8. Open a terminal under current directory, execute following command:
    1. `cd aws-sdk-layer/nodejs`
    2. `aws lambda publish-layer-version --layer-name cognito_layer --description "Cognito layer" --license-info "MIT" --compatible-runtimes nodejs18.x --zip-file fileb://../package.zip --region <specify a region>`, where `<specify a region>` should be replaced with the one correspoding to the region of the Lambda function just created.
9. Go back to the Lambda function coding page:
    1. Select `Add a layer`
    2. Select `Custom layers` under `Choose a layer`
    3. Select `cognito_layer`
    4. Select `Add`
10. Go to the `react` folder
    1. Chnage `VITE_COGNITO_REGION` to the region of the User Pool (eg. `us-east-1`)
    2. Change `VITE_COGNITO_USER_POOL_ID` to match the one shown under `User pool overview` -> `User pool ID` (eg. `us-east-1_OTyxlD7gH`)
    3. Change `VITE_COGNITO_CLIENT_ID` to match the one shown under `App Integration` Tab -> one of the App client (eg. `react`) -> `Client ID` (eg. `1qnsbceu4vtkdibn24sdh0qb6t`)