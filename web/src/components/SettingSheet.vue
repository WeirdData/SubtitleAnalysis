<template>
  <q-dialog
    ref="dialog"
    @hide="onDialogHide"
    position="bottom">
    <q-card class="q-dialog-plugin q-pa-sm">
      <q-card-section>
        <div class="text-h6">Setting</div>
      </q-card-section>
      <q-card-section class="q-mt-lg">
        <q-slider
          :min="minVal"
          :max="maxVal"
          :step="steps"
          :label-value="slideWords"
          label-always
          v-model="slideWords"
        >
        </q-slider>
        <div class="text-caption text-grey-6">
          Number of words to predict: {{ numberOfWords }}
        </div>
      </q-card-section>
      <q-card-section class="q-mt-lg">
        <q-slider
          :min="minTemp"
          :max="maxTemp"
          :step="stepTemp"
          :label-value="slideTemp"
          label-always
          v-model="slideTemp"
        >
        </q-slider>
        <div class="text-caption text-grey-6">
          Temperature for the predictions: {{ temperature }}
        </div>
        <div class="text-grey-6">more Temperature = more crazy predictions</div>
      </q-card-section>

      <q-card-actions class="justify-end q-mt-md">
        <q-btn label="Okay" flat color="primary" @click="hide()"></q-btn>
      </q-card-actions>

    </q-card>
  </q-dialog>

</template>

<script>

import {mapGetters, mapActions} from 'vuex'

export default {
  name: "SettingSheet",
  position: 'bottom',
  data() {
    return {
      steps: 1,
      minVal: 1,
      maxVal: 100,
      minTemp: 0.1,
      maxTemp: 2,
      stepTemp: 0.1
    }
  },
  mounted() {
    this.slideTemp = this.temperature;
    this.slideWords = this.numberOfWords;
  },
  computed: {
    ...mapGetters('serials', ['numberOfWords', 'temperature']),
    slideWords: {
      get: function () {
        return this.numberOfWords
      },
      set: function (newVal) {
        this.setNoOfWords(newVal)
      }
    },
    slideTemp: {
      get: function () {
        return this.temperature
      },
      set: function (newVal) {
        this.setTemperature(newVal)
      }
    }
  },
  methods: {
    ...mapActions('serials', ['setNoOfWords', 'setTemperature']),
    show() {
      this.$refs.dialog.show()
    },
    hide() {
      this.$refs.dialog.hide()
    },
    onDialogHide() {
      // required to be emitted
      // when QDialog emits "hide" event
      this.$emit('hide')
    },
    onOKClick() {
      // on OK, it is REQUIRED to
      // emit "ok" event (with optional payload)
      // before hiding the QDialog
      this.$emit('ok')
      // or with payload: this.$emit('ok', { ... })

      // then hiding dialog
      this.hide()
    },
    onCancelClick() {
      // we just need to hide dialog
      this.hide()
    }
  }
}
</script>

<style scoped>

</style>
