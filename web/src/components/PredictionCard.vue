<template>
  <div>
    <q-card>
      <q-card-section>
        <div class="text-caption">{{ subtitle }}</div>
        <div class="text-h6"> {{ title }}</div>
        <q-markup-table wrap-cells dense flat class="q-mt-lg">
          <tbody v-for="item in sentences" class="vertical-top">
          <tr>
            <td>{{ randomCharacter() }}</td>
            <td>{{ item }}</td>
          </tr>
          </tbody>
        </q-markup-table>
      </q-card-section>
    </q-card>
    <div class="text-caption text-grey-5
    justify-end float-right text-capitalize" v-if="sentences.length>1">
      FIRST {{ noOfWords }} WORDS
    </div>
  </div>


</template>

<script>

const gotChars = ["Tyrion", "Cersei", "Daenerys", "Jon", "Soldier", "Knight", "Sansa", "Arya", "Jaime", "Samwell", "Bronn"];
const bbtChars = ["Leonard", "Sheldon", "Penny", "Howard", "Raj", "Bernadette", "Amy"]


export default {
  name: "PredictionCard",
  props: ["title", "currentSerial", "sentences", "noOfWords"],
  data() {
    return {
      subtitle: "Dialogue will be generated for"
    }
  },
  methods: {
    randomCharacter() {
      let chars;
      if (this.currentSerial === "got") {
        chars = gotChars
      } else if (this.currentSerial === "bbt") {
        chars = bbtChars
      } else {
        return "Character " + Math.floor(Math.random() * 10)
      }
      return chars[Math.floor(Math.random() * chars.length)];
    },
  }
}
</script>

<style scoped>

</style>
