import { Amplify, Auth } from 'aws-amplify';

Amplify.configure({
  Auth: {
    // REQUIRED - Amazon Cognito Region
    region: import.meta.env.VITE_COGNITO_REGION,

    // OPTIONAL - Amazon Cognito User Pool ID
    userPoolId: import.meta.env.VITE_COGNITO_USER_POOL_ID,

    // OPTIONAL - Amazon Cognito Web Client ID (26-char alphanumeric string)
    userPoolWebClientId: import.meta.env.VITE_COGNITO_CLIENT_ID,

    // OPTIONAL - Hosted UI configuration
    oauth: {
      domain: import.meta.env.VITE_COGNITO_DOMAIN,
      scope: ['email', 'profile', 'openid', 'aws.cognito.signin.user.admin'],
      redirectSignIn: 'http://localhost:3000/',
      redirectSignOut: 'http://localhost:3000/',
      responseType: 'code' // or 'token', note that REFRESH token will only be generated when the responseType is code
    }
  }
});

export async function check_auth() {
  try {
    const user = await Auth.currentAuthenticatedUser({
      bypassCache: true // Optional, By default is false. If set to true, this call will send a request to Cognito to get the latest user data
    });
    // console.log(user)
    return true
  } catch (error) {
    // console.log(err)
      return false
  }
}

export async function signIn(username, password) {
  try {
    const user = await Auth.signIn(username, password);
    return {
      status: true,
      username: user.username,
      role: user.signInUserSession.accessToken.payload['cognito:groups'][0],
      accessToken: user.signInUserSession.accessToken.jwtToken,
      idToken: user.signInUserSession.idToken.jwtToken,
      refreshToken: user.signInUserSession.refreshToken.token,
    }
  } catch (error) {
    console.log('error signing in', error);
    return {
      status: false,
      error: error.toString()
    }
  }
}

export async function signUp(username, password, email) {
  try {
    const { user } = await Auth.signUp({
      username,
      password,
      attributes: {
        email,
      },
    });
    console.log(user)
    return {
      status: true,
      username: user.username,
      email: user.email,
    }
  } catch (error) {
    console.log('error signing up:', error);
    return {
      status: false,
      error: error.toString()
    }
  }
}

export async function confirmSignUp(username, code) {
  try {
    await Auth.confirmSignUp(username, code.toString());
    return {
      status: true,
    }
  } catch (error) {
    console.log('error confirming sign up', error);
    return {
      status: false,
      error: error.toString()
    }
  }
}

export async function resendConfirmationCode(username) {
  try {
    await Auth.resendSignUp(username);
    return {
      status: true,
    }
  } catch (err) {
    console.log('error resending code: ', err);
    return {
      status: false,
      error: err.toString()
    }
  }
}

export async function signOut() {
  try {
    await Auth.signOut();
    return {
      status: true,
    }
  } catch (error) {
    console.log('error signing out: ', error);
    return {
      status: false,
      error: error.toString()
    }
  }
}

export async function renew() {
  try {
    const user = Auth.currentSession();
    return {
      status: true,
      username: user.username,
      role: user.signInUserSession.accessToken.payload['cognito:groups'][0],
      accessToken: user.signInUserSession.accessToken.jwtToken,
      idToken: user.signInUserSession.idToken.jwtToken,
      refreshToken: user.signInUserSession.refreshToken.token,
    }
  } catch (error) {
    console.log('error signing out: ', error);
    return {
      status: false,
      error: error.toString()
    }
  }
}