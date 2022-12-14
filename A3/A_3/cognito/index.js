import { Callback, Context, PostConfirmationTriggerEvent } from "aws-lambda";
import AWS from "aws-sdk";

export async function main(event, _context, callback) {
  const { userPoolId, userName } = event;

  try {
    await addUserToGroup({
      userPoolId,
      username: userName,
      groupName: "user",
    });

    return callback(null, event);
  } catch (error) {
    return callback(error, event);
  }
}

export function addUserToGroup({
  userPoolId,
  username,
  groupName,
}) {
  const params = {
    GroupName: groupName,
    UserPoolId: userPoolId,
    Username: username,
  };

  const cognitoIdp = new AWS.CognitoIdentityServiceProvider();
  return cognitoIdp.addUserToGroup(params).promise();
}
