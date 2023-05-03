const slideMenuUsername = document.querySelector(".user-btn span");
const sendDataBtn = document.querySelector(".send-button");
const signoutBtn = document.querySelector(".signout-btn");


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
        console.log("Something wrong!")
    }
}


slideMenuUsername.after(getCookie("username"))
sendDataBtn.addEventListener("click", sendLampActionData)
signoutBtn.addEventListener("click", deleteCookies)