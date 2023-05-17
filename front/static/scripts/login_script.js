import * as utils from "./utils.js";

const signinText = document.querySelector(".title-text .login");
const signinForm = document.querySelector("form.login");
const signupForm = document.querySelector("form.signup");
const singinLabelBtn = document.querySelector("label.login");
const signupLabelBtn = document.querySelector("label.signup");
const innerForm = document.querySelector(".form-inner");
const signError = document.querySelector(".sign-error");
const login_size = `${signinForm.offsetHeight / 2}px`;
const signup_size = `${signinForm.offsetHeight}px`;

innerForm.style.height = login_size;


async function signup(event) {
    event.preventDefault();
    const myFormData = new FormData(event.target);
    const formDataObj = Object.fromEntries(myFormData.entries());

    let fetchOptions = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
        },
        body: JSON.stringify(formDataObj),
    };

    let response = await fetch(signupForm.action, fetchOptions);

    if (response.status != 200) {
        signError.innerText = await utils.errorInfo(response)
    } else {
        window.location.replace(utils.ROOT_PATH);
        document.cookie = `${utils.COOKIE_NAME_USER_ID}=${myFormData.get("email")}`;
    }
};

async function signin(event) {
    event.preventDefault();
    const myFormData = new FormData(event.target);

    let fetchOptions = {
        method: "POST",
        body: myFormData,
    };

    let response = await fetch(signinForm.action, fetchOptions);

    if (response.status != 200) {
        signError.innerText = await utils.errorInfo(response)
    } else {
        window.location.replace(utils.ROOT_PATH);
        document.cookie = `${utils.COOKIE_NAME_USER_ID}=${myFormData.get("username")}`;
    }
};


signupLabelBtn.onclick = (() => {
    signinForm.style.marginLeft = "-50%";
    signinText.style.marginLeft = "-50%";
    innerForm.style.height = signup_size;
    signError.innerText = "";

});
singinLabelBtn.onclick = (() => {
    signinForm.style.marginLeft = "0%";
    signinText.style.marginLeft = "0%";
    innerForm.style.height = login_size;
    signError.innerText = "";
});

signupForm.addEventListener('submit', signup);
signinForm.addEventListener('submit', signin);
