import * as utils from "./utils.js";

const slideMenuUsername = document.querySelector(".user-btn span");
const signoutBtn = document.querySelector(".signout-btn");
const sideMenu = document.querySelector(".side-menu");
const menuBtn = document.querySelector(".menu-btn");
const planBtn = document.querySelector(".plan-btn");
const userBtn = document.querySelector(".user-btn");
const mainContainer = document.querySelector(".main-container");
const planContainer = document.querySelector(".plan-container");
export const sendDataBtn = document.querySelector(".send-button");
export const responseStatus = document.querySelector(".sending-response-ok");


function showPlan() {
    mainContainer.hidden = true;
    planContainer.hidden = false;
}

function hidePlan() {
    mainContainer.hidden = false;
    planContainer.hidden = true;
}

function toggleHoverSideMenu() {
    let current_width = parseInt(sideMenu.style.width, 10)
    if (current_width < 300 || isNaN(current_width)) {
        sideMenu.style.width = "300px"
    } else {
        sideMenu.style.width = "60px"
    }
}

function hideSideMenu() {
    if (sideMenu.style.width == "300px") {
        sideMenu.style.width = "60px"
    }
}


async function sendLampActionData() {
    let data = {
        lamp_number: utils.getCookie(utils.COOKIE_NAME_LAMP_NUMBER),
        temperature: utils.getCookie(utils.COOKIE_NAME_COLOR_TEMP),
        brightness: utils.getCookie(utils.COOKIE_NAME_COLOR_BRIGHT)
    }

    let fetchOptions = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
        },
        body: JSON.stringify(data),
    };

    let response = await fetch(utils.LINK_LAMP_DATA, fetchOptions);

    if (response.status != 200) {
        responseStatus.className = "sending-response-err"
        responseStatus.innerHTML = await utils.errorInfo(response)
    } else {
        responseStatus.className = "sending-response-ok"
        responseStatus.innerHTML = "Ok"
    }
    responseStatus.classList.add("show-response")
    await utils.sleep(2000)
    responseStatus.classList.add("hide-response")
    await utils.sleep(300)
    responseStatus.classList.remove("show-response", "hide-response")
}


slideMenuUsername.after(utils.getCookie(utils.COOKIE_NAME_USER_ID))
sendDataBtn.addEventListener("click", sendLampActionData)
signoutBtn.addEventListener("click", utils.deleteCookies)
menuBtn.addEventListener("click", toggleHoverSideMenu)
planBtn.addEventListener("click", showPlan)
planBtn.addEventListener("click", hideSideMenu)
userBtn.addEventListener("click", hidePlan)
userBtn.addEventListener("click", hideSideMenu)