<template>
  <div>
    <v-row justify="center">
      <v-form>
        <v-text-field label="type here" v-model="inputWords"></v-text-field>
      </v-form>
    </v-row>
    <v-row justify="center" align="center">
      <v-btn :disabled="modelReady" @click="predict()">Ready</v-btn>
    </v-row>
    <v-row justify="center" class="ma-4">
      <v-card class="ma-4">
        <v-card-text>
          {{ predictedWords }}
        </v-card-text>
      </v-card>

    </v-row>
  </div>

</template>

<script>
import * as tf from '@tensorflow/tfjs';


export default {
  name: "ModelPredict",
  data() {
    return {
      modelReady: true,
      temperature: 0.8,
      noOfWords: 10,
      inputWords: "",
      predictedWords: "",
      ignoredWords: []
    }
  },
  mounted() {
    let tmp = this
    loadModel().then(function () {
      tmp.modelReady = false
    })
  },
  methods: {
    predict: function () {
      let tmp = this
      predictText(this.inputWords.trim(), this.temperature, this.noOfWords).then(function (e) {
        tmp.predictedWords = e[0]
        tmp.ignoredWords = e[1]
      })
    }
  }
}


let model;
let wordIds;
const sequence_length = 7;

async function loadModel() {
  model = await tf.loadLayersModel("model/model.json");
  wordIds = require("@/assets/raw/ids.json");
  console.log("Model Loaded");
}


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

async function predictText(input_words, temperature, noOfWords) {
  if (input_words.length === 0) {
    return ""
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

</script>

<style scoped>

</style>