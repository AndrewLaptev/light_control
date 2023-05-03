const slideMenuUsername = document.querySelector(".user-btn span");
const sendDataBtn = document.querySelector(".send-button");
const signoutBtn = document.querySelector(".signout-btn");
const responseStatus = document.querySelector(".sending-response-ok");


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
    return error["detail"]
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function sendLampActionData() {
    let data = {
        number: getCookie("lamp_numb"),
        temperature: getCookie("color_temp"),
        brightness: getCookie("color_bright")
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
    }
    responseStatus.classList.add("show-response")
    await sleep(2000)
    responseStatus.classList.add("hide-response")
    await sleep(300)
    responseStatus.classList.remove("show-response", "hide-response")
}


slideMenuUsername.after(getCookie("username"))
sendDataBtn.addEventListener("click", sendLampActionData)
signoutBtn.addEventListener("click", deleteCookies)