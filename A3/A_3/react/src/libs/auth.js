import request from "./request";

export function check() {
    return false;
}

export async function login() {
    return (new Promise((resolve) => {
        setTimeout(() => resolve('2342f2f1d131rf12'), 250);
    })).then((token) => {
        return "12355555555"
            });
}

export function register() {
    return false;
}

export function logout() {
    return false;
}

export function renew() {
    return false;
}