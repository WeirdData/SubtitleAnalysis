<template>
  <q-page padding class="justify-center q-pa-xl">
    <div class="row justify-center text-center">
      <p>
        Generate artificial dialogues for various serials based on your input.
        More details about this project can be found
        <router-link to="/about">here</router-link>
        .
      </p>

    </div>
    <div class="row justify-center text-grey-6 text-center">
      Select the serial and click on proceed.
    </div>
    <div class="row justify-center">
      <q-img
        :src="getImage(card.img)"
        class="my-img q-ma-lg"
        v-for="(card, key) in serialDetails"
        :key="key"
        @click="toggleSelection(key)">
        <div class="fit my-grad text-white text-center" :class="{hidden:!card.selected}">
          <q-icon name="done" style="font-size: 128px;" class="absolute-center"/>
        </div>
        <div
          class="absolute-bottom text-center"
          style="background: rgba(0,0,0,0.7)">
          {{ card.title }}
        </div>
      </q-img>
    </div>
    <div class="row justify-center q-ma-xl">
      <p class="col-12 text-center text-grey-6">Current Selection: {{ selectedCards }} </p>
      <q-btn
        :disable="disableBtn"
        :color="btnColor"
        label="Proceed"
        to="generate"
      />
      <q-page-sticky position="bottom-right" :offset="[18, 18]">
        <q-btn fab icon="keyboard_arrow_right"
               color="primary" padding="sm" v-if="hideFab"
               to="generate"
        />
      </q-page-sticky>
    </div>
  </q-page>
</template>

<script>
import {mapActions, mapGetters} from 'vuex'
import HomeCard from "components/HomeCard";


export default {
  name: "HomeView",
  components: {HomeCard},
  data() {
    return {
      disableBtn: true,
      btnColor: "grey"
    }
  },
  computed: {
    ...mapGetters('serials', ['serialDetails']),
    selectedCards: function () {
      for (let c in this.serialDetails) {
        if (this.serialDetails[c].selected) {
          this.disableBtn = false;
          this.btnColor = "primary";
          return this.serialDetails[c].title;
        }
      }
    },
    hideFab() {
      if (this.disableBtn) {
        return false
      }
      return this.$q.screen.lt.md;
    }
  },
  methods: {
    getImage(img) {
      return "images/" + img
    },
    ...mapActions('serials', ['toggleSelection'])
  }
}
</script>

<style scoped>
.my-img {
  width: 200px;
  height: auto;
  max-height: 300px;
  cursor: pointer;
}

.my-grad {
  background-color: rgba(0, 0, 0, 0.6);
}

</style>
