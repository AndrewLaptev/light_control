import * as utils from "./utils.js";


const signoutBtn = document.querySelector(".signout-btn");
const sideMenu = document.querySelector(".side-menu");
const menuBtn = document.querySelector(".menu-btn");
const userBtn = document.querySelector(".user-btn");
const planBtn = document.querySelector(".plan-btn");
const slideMenuUsername = document.querySelector(".user-btn span");

function toggleHoverSideMenu() {
    let current_width = parseInt(sideMenu.style.width, 10)
    if (current_width < 300 || isNaN(current_width)) {
        sideMenu.style.width = "300px"
    } else {
        sideMenu.style.width = "60px"
    }
}

function buttonBackground(button, pageName) {
    if (window.location.pathname.split("/").pop() == pageName) {
        button.style.background = "#014f9c";
    }
}

buttonBackground(userBtn, "main");
buttonBackground(planBtn, "plan");

slideMenuUsername.after(utils.getCookie(utils.COOKIE_NAME_USER_ID))
signoutBtn.addEventListener("click", utils.deleteCookies)
menuBtn.addEventListener("click", toggleHoverSideMenu)
