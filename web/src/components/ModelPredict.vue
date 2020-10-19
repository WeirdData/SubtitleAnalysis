<template>
  <div>
    <v-row class="ma-8">
      <v-col align-self="center" align="center">
        <v-card>
          <v-card-title class="justify-center">Input</v-card-title>
          <v-card-text>
            Type something below and click on predict
          </v-card-text>
          <v-row justify="center">
            <v-form>
              <v-text-field label="Seed Words" v-model="inputWords"></v-text-field>
            </v-form>
          </v-row>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn @click="predict()" text>Predict</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
      <v-col>

        <v-card style="height: 100%">
          <v-progress-linear
              color="deep-purple accent-4"
              rounded
              height="6"
              absolute
              :active="showLoading"
              :indeterminate="showLoading"
          ></v-progress-linear>
          <v-card-title class="align-center">Prediction</v-card-title>
          <v-card-text>Text Prediction will Appear Below</v-card-text>
          <v-card-text>
            {{ predictedWords }}
          </v-card-text>

        </v-card>
      </v-col>
    </v-row>
    <v-row class="ma-8">
      <v-col>
        <v-card>
          <v-card-title class="justify-center">
            Settings
          </v-card-title>
          <v-row class="ma-8">
            <v-slider thumb-label="always"
                      v-model="noOfWords"
                      min="5"
                      max="100"
                      label="No of Words">
              <template v-slot:append>
                <v-text-field
                    v-model="noOfWords"
                    class="mt-0 pt-0"
                    hide-details
                    single-line
                    type="number"
                    style="width: 60px"
                ></v-text-field>
              </template>
            </v-slider>
          </v-row>
          <v-row class="ma-8">
            <v-slider thumb-label="always"
                      v-model="temperature"
                      min="0.1"
                      step="0.1"
                      max="2"
                      label="Temperature">
              <template v-slot:append>
                <v-text-field
                    v-model="temperature"
                    class="mt-0 pt-0"
                    hide-details
                    single-line
                    type="number"
                    style="width: 60px"
                ></v-text-field>
              </template>
            </v-slider>
          </v-row>
        </v-card>
      </v-col>
      <v-col>
        <v-card>
          <v-card-title class="justify-center">
            Instructions
          </v-card-title>
          <v-card-text>
            here
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import MLWorker from '@/tensor-worker'

export default {
  name: "ModelPredict",
  data() {
    return {
      temperature: 0.8,
      noOfWords: 25,
      inputWords: "",
      predictedWords: "N/A",
      ignoredWords: [],
      showLoading: false
    }
  },
  mounted() {
    MLWorker.worker.onmessage = event => {
      this.predictedWords = event.data[0];
      this.ignoredWords = event.data[1];
      this.showLoading = false;
    }
  },
  methods: {
    predict() {
      this.showLoading = true;
      this.predictedWords = "...";
      MLWorker.send({
        input_words: this.inputWords.trim(),
        temperature: this.temperature,
        noOfWords: this.noOfWords
      });
    }
  }
}


</script>

<style scoped>

</style>