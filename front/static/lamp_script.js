const inputContainer = document.querySelector(".input-container");
const input = inputContainer.firstElementChild.nextElementSibling;
const minus = inputContainer.firstElementChild;
const plus = inputContainer.lastElementChild;


function changeNumber(e) {
    if (e.target == minus) {
        if (input.value > 1) {
            input.value--;
        }
    } else if (e.target == plus) {
        if (input.value < 8) {
            input.value++;
        }
    }
    document.cookie = `${COOKIE_NAME_LAMP_NUMBER}=${input.value}`;
}

async function getLampData(e) {
    if (e.target == minus || e.target == plus) {
        response = await fetch('light/lamp-data?' + new URLSearchParams
            (
                {
                    lamp_number: input.value
                }
            )
        )
        lamp_data = await response.json()

        lightTempSlider.setSlider(lamp_data[COOKIE_NAME_COLOR_TEMP])
        lightBrightSlider.setSlider(lamp_data[COOKIE_NAME_COLOR_BRIGHT])
    }
}


inputContainer.addEventListener("click", changeNumber);
inputContainer.addEventListener("click", getLampData);

if (lamp_numb = getCookie(COOKIE_NAME_LAMP_NUMBER)) {
    input.value = lamp_numb
} else {
    document.cookie = `${COOKIE_NAME_LAMP_NUMBER}=${document.querySelector(".lamp-num-container input").value}`;
}
