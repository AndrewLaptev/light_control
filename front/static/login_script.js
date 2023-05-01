const loginText = document.querySelector(".title-text .login");
const signinForm = document.querySelector("form.login");
const signupForm = document.querySelector("form.signup");
const loginLabelBtn = document.querySelector("label.login");
const signupLabelBtn = document.querySelector("label.signup");
const innerForm = document.querySelector(".form-inner");
const signError = document.querySelector(".sign-error");

const LOGIN_SIZE = `${signinForm.offsetHeight / 2}px`;
const SIGNUP_SIZE = `${signinForm.offsetHeight}px`;
const TOKEN_NAME = 'light_control_token'


innerForm.style.height = LOGIN_SIZE;

signupLabelBtn.onclick = (() => {
    signinForm.style.marginLeft = "-50%";
    loginText.style.marginLeft = "-50%";
    innerForm.style.height = SIGNUP_SIZE;
    signError.innerText = "";

});
loginLabelBtn.onclick = (() => {
    signinForm.style.marginLeft = "0%";
    loginText.style.marginLeft = "0%";
    innerForm.style.height = LOGIN_SIZE;
    signError.innerText = "";
});


async function errorInfo(response) {
    error = await response.json()
    signError.innerText = error["detail"]
}

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

    response = await fetch(signupForm.action, fetchOptions);

    if (response.status != 200) {
        await errorInfo(response)
    } else {
        window.location.replace("/");
    }
};

signinForm.addEventListener('submit', signin);
async function signin(event) {
    event.preventDefault();
    const myFormData = new FormData(event.target);

    let fetchOptions = {
        method: "POST",
        body: myFormData,
    };

    response = await fetch(signinForm.action, fetchOptions);

    if (response.status != 200) {
        await errorInfo(response)
    } else {
        window.location.replace("/");
    }
};
