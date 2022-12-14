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

export function check_auth() {
    return false;
}

export function check_permission() {
    return false;
}

export async function signIn() {
    try {
        const user = await Auth.signIn(username, password);
    } catch (error) {
        console.log('error signing in', error);
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
            error: error.message
        }
    }
}

export async function confirmSignUp(username, code) {
    try {
        await Auth.confirmSignUp(username, code);
        console.log('success');
    } catch (error) {
        console.log('error confirming sign up', error);
    }
}

export async function resendConfirmationCode(username) {
    try {
        await Auth.resendSignUp(username);
        console.log('code resent successfully');
    } catch (err) {
        console.log('error resending code: ', err);
    }
}

export async function signOut() {
    try {
        await Auth.signOut();
    } catch (error) {
        console.log('error signing out: ', error);
    }
}

export function renew() {
    return false;
}