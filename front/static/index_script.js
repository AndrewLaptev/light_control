const slideMenuUsername = document.querySelector(".user-btn span");
const sendDataBtn = document.querySelector(".send-button");
const signoutBtn = document.querySelector(".signout-btn");
const responseStatus = document.querySelector(".sending-response-ok");

const COOKIE_NAME_LAMP_NUMBER = "lamp_number"
const COOKIE_NAME_COLOR_TEMP = "temperature"
const COOKIE_NAME_COLOR_BRIGHT = "brightness"
const COOKIE_NAME_USER_ID = "username"


function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

function deleteCookies() {
    var Cookies = document.cookie.split(';');
    for (var i = 0; i < Cookies.length; i++) {
        document.cookie = Cookies[i] + "=;expires=" + new Date(0).toUTCString();
    }
}

async function errorInfo(response) {
    error = await response.json()
    if (typeof error["detail"] == "object") {
        return "Something went wrong!"
    } else {
        return error["detail"]
    }
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function sendLampActionData() {
    let data = {
        lamp_number: getCookie(COOKIE_NAME_LAMP_NUMBER),
        temperature: getCookie(COOKIE_NAME_COLOR_TEMP),
        brightness: getCookie(COOKIE_NAME_COLOR_BRIGHT)
    }

    let fetchOptions = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
        },
        body: JSON.stringify(data),
    };

    response = await fetch("light/lamp-data", fetchOptions);

    if (response.status != 200) {
        responseStatus.className = "sending-response-err"
        responseStatus.innerHTML = await errorInfo(response)
    } else {
        responseStatus.className = "sending-response-ok"
        responseStatus.innerHTML = "Ok"
    }
    responseStatus.classList.add("show-response")
    await sleep(2000)
    responseStatus.classList.add("hide-response")
    await sleep(300)
    responseStatus.classList.remove("show-response", "hide-response")
}


slideMenuUsername.after(getCookie(COOKIE_NAME_USER_ID))
sendDataBtn.addEventListener("click", sendLampActionData)
signoutBtn.addEventListener("click", deleteCookies)