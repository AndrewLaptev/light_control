import * as utils from "./utils.js";
import { responseStatus } from "./index_script.js";
import { lightTempSlider, lightBrightSlider } from "./slider_script.js";

const inputContainer = document.querySelector(".input-container");
const input = inputContainer.firstElementChild.nextElementSibling;
const minus = inputContainer.firstElementChild;
const plus = inputContainer.lastElementChild;
var lampNumState = 1;


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
    document.cookie = `${utils.COOKIE_NAME_LAMP_NUMBER}=${input.value}`;
}

async function getLampData(e) {
    if (input.value != lampNumState) {
        lampNumState = input.value;

        if (e.target == minus || e.target == plus) {
            let response = await fetch(utils.LINK_LAMP_DATA + '?' + new URLSearchParams
                (
                    {
                        lamp_number: input.value
                    }
                )
            )

            if (response.status != 200) {
                responseStatus.className = "sending-response-err"
                responseStatus.innerHTML = await utils.errorInfo(response)

                responseStatus.classList.add("show-response")
                await sleep(2000)
                responseStatus.classList.add("hide-response")
                await sleep(300)
                responseStatus.classList.remove("show-response", "hide-response")
            } else {
                let lamp_data = await response.json()

                lightTempSlider.setSlider(lamp_data[utils.COOKIE_NAME_COLOR_TEMP])
                lightBrightSlider.setSlider(lamp_data[utils.COOKIE_NAME_COLOR_BRIGHT])
            }

        }
    }
}

async function initLampData() {
    let response = await fetch(utils.LINK_LAMP_DATA + '?' + new URLSearchParams
        (
            {
                lamp_number: input.value
            }
        )
    )
    if (response.status != 200) {
        console.log(response.statusText)
    } else {
        let lamp_data = await response.json()

        lightTempSlider.setSlider(lamp_data[utils.COOKIE_NAME_COLOR_TEMP])
        lightBrightSlider.setSlider(lamp_data[utils.COOKIE_NAME_COLOR_BRIGHT])
    }
}


inputContainer.addEventListener("click", changeNumber);
inputContainer.addEventListener("click", getLampData);

if (utils.getCookie(utils.COOKIE_NAME_LAMP_NUMBER)) {
    input.value = utils.getCookie(utils.COOKIE_NAME_LAMP_NUMBER)
} else {
    initLampData();
    document.cookie = `${utils.COOKIE_NAME_LAMP_NUMBER}=${document.querySelector(".lamp-num-container input").value}`;
}
