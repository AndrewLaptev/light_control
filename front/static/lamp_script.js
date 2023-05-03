const inputContainer = document.querySelector(".input-container");
const input = inputContainer.firstElementChild.nextElementSibling;
const minus = inputContainer.firstElementChild;
const plus = inputContainer.lastElementChild;


function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

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
    document.cookie = `lamp_numb=${input.value}`;
}

async function getLampData(e) {
    response = await fetch('light/lamp-data?' + new URLSearchParams
        (
            {
                lamp_number: input.value
            }
        )
    )
    lamp_data = await response.json()

    lightTempSlider.setSlider(lamp_data["temperature"])
    lightBrightSlider.setSlider(lamp_data["brightness"])
}


inputContainer.addEventListener("click", changeNumber);
inputContainer.addEventListener("click", getLampData);

if (lamp_numb = getCookie("lamp_numb")) {
    input.value = lamp_numb
}
