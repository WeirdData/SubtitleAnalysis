import * as tf from '@tensorflow/tfjs';

tf.setBackend('cpu');

let model;
let wordIds;
const sequence_length = 7;

async function loadModel() {
    model = await tf.loadLayersModel("/model/model.json");
    return model
}

loadModel().then(r => {
    model = r;
    wordIds = require("@/assets/raw/ids.json");
    console.log("Model Loaded");
})

self.addEventListener('message', function (me) {
    let e = me.data.message;
    let data = predictText(e.input_words, e.temperature, e.noOfWords)
    postMessage(data);
}, false);


function process(number, temperature) {
    number = Math.log(number) / temperature
    number = Math.exp(number)
    return number
}

function swap(json) {
    const ret = {};
    for (const key in json) {
        ret[json[key]] = key;
    }
    return ret;
}

function predictText(input_words, temperature, noOfWords) {
    if (input_words.length === 0) {
        return ["N/A", []]
    }
    input_words = input_words.toLowerCase().split(" ")
    let currentWords = []
    let predictedWords = []
    let ignoredWords = []
    for (let w of input_words) {
        if (w in wordIds) {
            currentWords.push(wordIds[w])
            predictedWords.push(wordIds[w])
        } else {
            ignoredWords.push(w)
        }
    }

    for (const i of Array(noOfWords).keys()) {
        while (currentWords.length < sequence_length) {
            currentWords.unshift(0)
        }
        while (currentWords.length > sequence_length) {
            currentWords.shift()
        }
        let prediction = model.predict(tf.tensor([currentWords])).arraySync()[0];
        prediction = prediction.map(function (e) {
            return process(e, temperature)
        });
        const predSum = prediction.reduce(function (a, b) {
            return a + b;
        });
        prediction = prediction.map(function (e) {
            return e / predSum
        });
        let prediction_id = tf.multinomial(prediction, 1, null, true).arraySync()[0]
        currentWords.push(prediction_id)
        predictedWords.push(prediction_id)
    }

    let id2char = swap(wordIds)
    let convertedWords = ""
    for (let k of predictedWords) {
        if (k !== 0) {
            let cw = id2char[k]
            if (["'m", "n't", "'s", "'ll", ",", "?", "."].indexOf(cw) !== -1) {
                convertedWords += cw
            } else {
                convertedWords += " " + cw
            }

        }
    }
    return [convertedWords, ignoredWords]
}
