const loginText = document.querySelector(".title-text .login");
const loginForm = document.querySelector("form.login");
const signupForm = document.querySelector("form.signup");
const loginLabelBtn = document.querySelector("label.login");
const signupLabelBtn = document.querySelector("label.signup");
const innerForm = document.querySelector(".form-inner");

const LOGIN_SIZE = `${loginForm.offsetHeight / 2}px`;
const SIGNUP_SIZE = `${loginForm.offsetHeight}px`;
const TOKEN_NAME = 'light_control_token'


innerForm.style.height = LOGIN_SIZE;

signupLabelBtn.onclick = (() => {
    loginForm.style.marginLeft = "-50%";
    loginText.style.marginLeft = "-50%";
    innerForm.style.height = SIGNUP_SIZE;
});
loginLabelBtn.onclick = (() => {
    loginForm.style.marginLeft = "0%";
    loginText.style.marginLeft = "0%";
    innerForm.style.height = LOGIN_SIZE;
});

signupForm.addEventListener('submit', signup);
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
    await fetch(signupForm.action, fetchOptions);
    window.location.replace("/");
};
