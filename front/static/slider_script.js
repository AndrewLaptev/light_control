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

let lightTempOptions = {
    min: 2700,
    max: 6500,
    cur: (color_temp = getCookie(COOKIE_NAME_COLOR_TEMP)) ? color_temp : 2700,
    measure: 'K'
}

let lightBrightOptions = {
    min: 0,
    max: 100,
    cur: (color_temp = getCookie(COOKIE_NAME_COLOR_BRIGHT)) ? color_temp : 0,
    measure: '%'
}

let lightTempSlider = new Slider(lightTempElement, lightTempValueElement, COOKIE_NAME_COLOR_TEMP, sendDataBtn, lightTempOptions)
let lightBrightSlider = new Slider(lightBrightElement, lightBrightValueElement, COOKIE_NAME_COLOR_BRIGHT, sendDataBtn, lightBrightOptions)

lightTempSlider.init()
lightBrightSlider.init()
