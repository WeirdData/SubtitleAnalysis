<template>
  <q-page padding class="justify-center q-pa-xl">
    <div v-if="currentSerial==null">
      <div class="row text-body1 text-center justify-center q-ma-lg">
        You have not selected any serial yet. Please go back to the home and select one!
      </div>
      <div class="row justify-center q-ma-xl">
        <q-btn label="Go Home" class="col-1" color="primary" to="/"></q-btn>
      </div>
    </div>
    <div v-if="currentSerial!==null">
      <div class="row justify-center">
        <div class="column col-4">
          <PredictionCard
            :current-serial="currentSerial"
            :title="serialDetails[currentSerial].title"
            :sentences="predictedWords"
            :no-of-words="numberOfWords"
          />
        </div>

        <q-btn label="press" @click="predict()"></q-btn>
      </div>
    </div>

  </q-page>
</template>

<script>
import {mapGetters} from 'vuex'
import MLWorker from "../tensor-worker"
import PredictionCard from "components/PredictionCard";

export default {
  name: "PredictionRoom",
  components: {PredictionCard},
  data() {
    return {
      predictedWords: ["N/A"],
      ignoredWords: [],
      numberOfWords: 30
    }
  },
  mounted() {
    MLWorker.worker.onmessage = event => {
      this.predictedWords = event.data[0];
      this.ignoredWords = event.data[1];
    }
  },
  computed: {
    ...mapGetters('serials', ['currentSerial', 'serialDetails']),
  },
  methods: {
    predict() {
      MLWorker.send({
        input_words: "we are",
        temperature: 0.5,
        noOfWords: this.numberOfWords,
        serial: this.currentSerial
      });
    }
  }
}
</script>

<style scoped>

</style>
