class Slider {
    constructor(rangeElement, valueElement, options) {
        this.rangeElement = rangeElement
        this.valueElement = valueElement
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
        return parseFloat(value) + this.options.measure
    }

    updateSlider(newValue) {
        this.valueElement.innerHTML = this.asSome(this.rangeElement.value)
    }
};



let lightTempElement = document.querySelector('.light-temperature [type="range"]')
let lightTempValueElement = document.querySelector('.light-temperature__value span')
let lightBrightElement = document.querySelector('.light-brightness [type="range"]')
let lightBrightValueElement = document.querySelector('.light-brightness__value span')

let lightTempOptions = {
    min: 2000,
    max: 6800,
    cur: 2000,
    measure: 'K'
}

let lightBrightOptions = {
    min: 0,
    max: 100,
    cur: 0,
    measure: '%'
}

if (lightTempElement) {
    let lightTempSlider = new Slider(lightTempElement, lightTempValueElement, lightTempOptions)
    let lightBrightSlider = new Slider(lightBrightElement, lightBrightValueElement, lightBrightOptions)

    lightTempSlider.init()
    lightBrightSlider.init()
}