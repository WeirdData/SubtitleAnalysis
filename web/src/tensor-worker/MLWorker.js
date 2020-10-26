import * as tf from '@tensorflow/tfjs';

tf.setBackend('cpu').then(() => {
  console.log("Backend set to CPU")
});

let all_models = {};
let all_wordIds = {};
const sequence_length = 7;

async function loadModel(name) {
  if (all_models.hasOwnProperty(name)) {
    console.log("Model for " + name + " is already loaded")
    return null
  }
  all_models[name] = await tf.loadLayersModel("/models/" + name + "/model.json");
  all_wordIds[name] = require("assets/raw/" + name + ".json")
  console.log("Models and WorldLists for " + name + " Loaded");
  return null
}

self.addEventListener('message', function (me) {
  let e = me.data.message;
  loadModel(e.serial).then(() => {
    let model = all_models[e.serial];
    let wordIds = all_wordIds[e.serial];
    let data = predictText(e.input_words, e.temperature, e.noOfWords, wordIds, model)
    postMessage(data);
  })

}, false);


function process(number, temperature) {
  number = Math.log(number) / temperature
  number = Math.exp(number)
  return number
}

function swap(json) {
  const ret = {};
  for (const key in json) {
    if (json.hasOwnProperty(key)) {
      ret[json[key]] = key;
    }
  }
  return ret;
}

function predictText(input_words, temperature, noOfWords, wordIds, model) {
  if (input_words.length === 0) {
    return [["??"], []]
  }
  input_words = input_words.toLowerCase().split(" ")
  let currentWords = []
  let predictedWords = []
  let ignoredWords = []
  for (let w of input_words) {

    if (wordIds.hasOwnProperty(w)) {
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
      if ([".", "?"].indexOf(convertedWords.slice(-1)) !== -1) {
        convertedWords += "/n"
      }
    }
  }
  convertedWords += "..."
  return [convertedWords.split("/n"), ignoredWords]
}
