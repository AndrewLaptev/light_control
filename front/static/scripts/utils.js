export const COOKIE_NAME_USER_ID = "username"
export const COOKIE_NAME_LAMP_NUMBER = "lamp_number"
export const COOKIE_NAME_COLOR_TEMP = "temperature"
export const COOKIE_NAME_COLOR_BRIGHT = "brightness"

export const LINK_ROOT = "/light-control/"
export const LINK_LAMP_DATA = LINK_ROOT + "light/lamp-data"


export function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

export function deleteCookies() {
    const cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
        document.cookie = cookies[i] + "=;expires=" + new Date(0).toUTCString();
    }
}

export async function errorInfo(response) {
    const error = await response.json()
    if (typeof error["detail"] == "object") {
        return "Something went wrong!"
    } else {
        return error["detail"]
    }
}