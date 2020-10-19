<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <v-container>
      <v-row>
        <v-form>
          <v-text-field label="type here" v-model="inputWords"></v-text-field>
        </v-form>
      </v-row>
      <v-row>

        <v-btn @click="makePrediction()">Predict</v-btn>
      </v-row>

      Input Words : {{inputWords}} <br/>
      Predicted Words: {{predictedWords}}
      <br/><br/>
      <span v-for="item in predictedSentence">
        {{item}} <br/>
      </span>

    </v-container>


  </div>
</template>

<script>


import * as tf from '@tensorflow/tfjs';

let model;
let wordIds;

async function loadModel(){
  model = await tf.loadLayersModel("model/model.json");
  wordIds = require("@/assets/raw/ids.json")
  console.log("Model Loaded")
}


function swap(json){
  const ret = {};
  for(const key in json){
    ret[json[key]] = key;
  }
  return ret;
}

export default {
  name: 'HelloWorld',
  data :()=>({
    inputWords:"",
    predictedWords:"None",
    predictedSentence:[],
    temperature:0.4
  }),
  props: {
    msg: String,
  },
  methods: {
    makePrediction(){
      let sentence =[];
      for (const word of this.inputWords.split(" ")){
        if (word in  wordIds){
          sentence.push(wordIds[word])
        }else {
          this.predictedWords = "Unknown word"
        }
      }
      let inWords = tf.expandDims(sentence,0)
      let id2word = swap(wordIds)
      model.resetStates()
      let prediction;
      let prediction_id;
      let newSentence = [];
      for (const i of Array(25).keys()){
        prediction = model.predict(inWords);
        prediction = tf.squeeze(prediction,0);
        prediction = prediction.arraySync();
        prediction = prediction.map( (v,i) => v.map( x=> x = x/this.temperature ) );
        prediction = tf.tensor(prediction);
        prediction_id = tf.multinomial(prediction,1).arraySync();
        prediction_id = prediction_id[prediction_id.length-1][0];
        if (prediction_id in id2word){
          newSentence.push(id2word[prediction_id]);
        }else {
          console.log("Unknown ID: "+ prediction_id );
        }
        prediction = tf.expandDims([prediction_id], 0);
      }
      let dialogue = [];
      let currentStr = "";
      for (let m of sentence){
        currentStr += " "+ id2word[m];
      }
      for (let m of newSentence){
        currentStr += " " + m;
        if (m === "." || m === "?" || m==="!") {
          dialogue.push(currentStr);
          currentStr = "";
        }
      }
      dialogue.push(currentStr);
      this.predictedSentence = dialogue
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
