import * as utils from "./utils.js";

// Main page
export const sendDataBtn = document.querySelector(".send-button");
export const responseStatus = document.querySelector(".sending-response-ok");

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

    let response = await fetch(utils.API_LIGHT_PATH + 'lamp-data', fetchOptions);

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

sendDataBtn.addEventListener("click", sendLampActionData)


// Lamp manage

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
            let response = await fetch(utils.API_LIGHT_PATH + 'lamp-data' + '?' + new URLSearchParams
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
                await utils.sleep(2000)
                responseStatus.classList.add("hide-response")
                await utils.sleep(300)
                responseStatus.classList.remove("show-response", "hide-response")
            } else {
                let lamp_data = await response.json()

                lightTempSlider.setSlider(lamp_data[utils.COOKIE_NAME_COLOR_TEMP])
                lightBrightSlider.setSlider(lamp_data[utils.COOKIE_NAME_COLOR_BRIGHT])
            }

        }
    }
}

function changeNumberKeys(e) {
    if (e.key == "ArrowRight") {
        document.getElementById("plus").click()
    } else if (e.key == "ArrowLeft") {
        document.getElementById("minus").click()
    } else if (e.key == "Enter") {
        document.querySelector(".send-button").click()
    }
}

async function initLampData() {
    let response = await fetch(utils.API_LIGHT_PATH + 'lamp-data' + '?' + new URLSearchParams
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
document.addEventListener("keydown", changeNumberKeys);

if (utils.getCookie(utils.COOKIE_NAME_LAMP_NUMBER)) {
    input.value = utils.getCookie(utils.COOKIE_NAME_LAMP_NUMBER)
} else {
    initLampData();
    document.cookie = `${utils.COOKIE_NAME_LAMP_NUMBER}=${document.querySelector(".lamp-num-container input").value}`;
}


// Slider manage

class Slider {
    constructor(rangeElement, valueElement, sliderName, sendDataBtn, options) {
        this.rangeElement = rangeElement
        this.valueElement = valueElement
        this.sliderName = sliderName
        this.sendDataBtn = sendDataBtn
        this.options = options

        // Attach a listener to "change" event
        this.rangeElement.addEventListener('input', this.updateSlider.bind(this))
    }

    // Initialize the slider
    init() {
        this.rangeElement.setAttribute('min', this.options.min)
        this.rangeElement.setAttribute('max', this.options.max)
        this.rangeElement.value = this.options.cur

        this.updateSlider()
    }

    // Format
    asSome(value) {
        return parseFloat(value)
    }

    updateSlider() {
        let val = this.asSome(this.rangeElement.value)
        this.valueElement.innerHTML = val + this.options.measure
        document.cookie = `${this.sliderName}=${val}`;
    }

    setSlider(newValue) {
        let val = this.asSome(newValue)
        this.valueElement.innerHTML = val + this.options.measure
        document.cookie = `${this.sliderName}=${val}`;
        this.rangeElement.value = val;
    }
};


let lightTempElement = document.querySelector('.light-temperature [type="range"]')
let lightTempValueElement = document.querySelector('.light-temperature__value span')
let lightBrightElement = document.querySelector('.light-brightness [type="range"]')
let lightBrightValueElement = document.querySelector('.light-brightness__value span')

let color_temp = utils.getCookie(utils.COOKIE_NAME_COLOR_TEMP)
let color_bright = utils.getCookie(utils.COOKIE_NAME_COLOR_BRIGHT)

let lightTempOptions = {
    min: 2700,
    max: 6500,
    cur: color_temp ? color_temp : 2700,
    measure: 'K'
}

let lightBrightOptions = {
    min: 0,
    max: 100,
    cur: color_bright ? color_bright : 0,
    measure: '%'
}

export var lightTempSlider = new Slider(lightTempElement, lightTempValueElement, utils.COOKIE_NAME_COLOR_TEMP, sendDataBtn, lightTempOptions)
export var lightBrightSlider = new Slider(lightBrightElement, lightBrightValueElement, utils.COOKIE_NAME_COLOR_BRIGHT, sendDataBtn, lightBrightOptions)

lightTempSlider.init()
lightBrightSlider.init()