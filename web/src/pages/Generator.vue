<template>
  <q-page padding class="justify-center q-pa-xl">
    <div v-if="currentSerial==null">
      <div class="row text-body1 text-center justify-center q-ma-lg">
        You have not selected any serial yet. Please go back to the home and select one!
      </div>
      <div class="row justify-center q-ma-xl">
        <q-btn label="Go Home" color="primary" to="/"></q-btn>
      </div>
    </div>
    <div v-if="currentSerial!==null">
      <form class="row justify-center q-mb-lg">
        <q-input
          ref="inputWords"
          outlined
          @keydown.enter.prevent="predict()"
          v-model="inputView"
          label="Provide starting words here"
          class="column col-xs-12 col-md-8 col-lg-5"
          :rules="[ val => val && val.length > 0 || 'Please provide input seed']"
        >
          <template v-slot:append>
            <q-icon name="far fa-question-circle" @click="showInfo()" class="cursor-pointer" size="sm"/>
          </template>
        </q-input>
      </form>

      <div class="row justify-center">
        <div class="column col-xs-12 col-md-8 col-lg-5">
          <q-linear-progress query color="warning" v-if="showProgress"/>
          <PredictionCard
            :current-serial="currentSerial"
            :title="serialDetails[currentSerial].title"
            :sentences="predictedWords"
          />
          <div class="text-caption text-grey-5 q-mt-xs items-center
              justify-end text-right" v-if="predictedWords.length>1">
            FIRST {{ ncw }} WORDS
            <q-btn dense size="sm" flat round icon="info" @click="showSettings()">
              <q-tooltip>
                You can adjust this in the settings.
              </q-tooltip>
            </q-btn>
          </div>
        </div>
      </div>
      <div class="row items-center justify-center text-red-4 q-my-sm" v-if="ignoredWords.length !==0">
        Ignored words: {{ ignoredWords }}
        <q-icon
          color="red-4"
          name="far fa-question-circle"
          @click="showIgnore()"
          class="cursor-pointer q-ml-sm" size="xs"/>
      </div>
      <div class="row justify-center q-ma-xl">
        <div class="row justify-end col-xs-12 col-md-8 col-lg-5">
          <q-btn outline color="primary" label="Generate" @click="predict()" class="q-mx-sm"></q-btn>
          <q-btn flat round color="primary" icon="settings" @click="showSettings()" class="mobile-only"></q-btn>
          <q-btn outline color="primary" label="settings" @click="showSettings()" class="desktop-only"></q-btn>
        </div>
      </div>
    </div>

  </q-page>
</template>

<script>
import {mapGetters, mapActions} from 'vuex'
import MLWorker from "../tensor-worker"
import PredictionCard from "components/PredictionCard";
import SettingSheet from "components/SettingSheet";

let oldWords = null;
export default {
  name: "PredictionRoom",
  components: {SettingSheet, PredictionCard},
  data() {
    return {
      inputView: "",
      predictedWords: ["??"],
      ignoredWords: [],
      showProgress: false
    }
  },
  mounted() {
    MLWorker.worker.onmessage = event => {
      this.predictedWords = event.data[0];
      this.ignoredWords = event.data[1];
      this.showProgress = false;
    }
    this.inputView = this.inputWords
    if (this.inputView.length > 1) {
      this.showProgress = true;
      MLWorker.send({
        input_words: this.getCurrentInput(),
        temperature: this.temperature,
        noOfWords: this.numberOfWords,
        serial: this.currentSerial
      });
    }
  },
  computed: {
    ...mapGetters('serials', ['currentSerial', 'serialDetails', 'numberOfWords', 'temperature', 'inputWords']),
    ncw: function () {
      if (oldWords === null) {
        oldWords = this.numberOfWords;
      }
      if (this.numberOfWords !== oldWords) {
        this.predictedWords = ["??"];
        this.ignoredWords = [];
        oldWords = this.numberOfWords;
      }
      return this.numberOfWords
    }
  },
  methods: {
    ...mapActions('serials', ['setInputWords']),
    predict() {
      this.$refs.inputWords.validate()
      if (this.$refs.inputWords.hasError) {
        return
      }
      this.showProgress = true;
      MLWorker.send({
        input_words: this.getCurrentInput(),
        temperature: this.temperature,
        noOfWords: this.numberOfWords,
        serial: this.currentSerial
      });
    },
    getCurrentInput() {
      this.setInputWords(this.inputView.trim())
      return this.inputView.trim()
    },
    showSettings() {
      this.$q.dialog({
        component: SettingSheet,
        parent: this,
      }).onOk(() => {
      })
    },
    showInfo() {
      this.$q.dialog({
        title: "Input Information",
        message: "Our AI model will take this as a seed sequence and predict the further dialogue." +
          "This will ignore all the words which did not appear in respective serial. Keep space between " +
          "words and punctuation marks."
      })
    },
    showIgnore() {
      this.$q.dialog({
        title: "Ignored Words",
        message: "Currently, our model can only consider words which were used in respective serials. Hence, " +
          "all new words will be ignored for the dialogue generation. If you want to use punctuation marks, " +
          "please use space before using them."
      })
    }

  }
}
</script>

<style scoped>

</style>
