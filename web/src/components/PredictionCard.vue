<template>
  <div>

    <q-card>
      <q-card-section>
        <div class="text-caption text-grey-6">{{ subtitle }}</div>
        <div class="text-h6"> {{ title }}</div>
        <q-markup-table wrap-cells dense flat class="q-mt-lg">
          <tbody v-for="item in sentences" class="vertical-top">
          <tr>
            <td class="text-grey-8 text-right" v-if="item!=='??'">{{ randomCharacter(item) }}</td>
            <td>{{ item }}</td>
          </tr>
          </tbody>
        </q-markup-table>
      </q-card-section>
    </q-card>
  </div>


</template>

<script>


const gotChars = ["Tyrion", "Cersei", "Daenerys", "Jon", "Soldier", "Knight", "Sansa", "Arya", "Jaime", "Samwell", "Bronn"];
const bbtChars = ["Leonard", "Sheldon", "Penny", "Howard", "Raj", "Bernadette", "Amy"]


export default {
  name: "PredictionCard",
  props: ["title", "currentSerial", "sentences"],
  computed: {
    subtitle: function () {
      if (this.sentences.length > 1) {
        return "Dialogues generated for"
      } else {
        return "Use 'Generate' button to generate some dialogues for"
      }
    }
  },
  methods: {
    randomCharacter(item) {
      if (String(item).includes('hodor')){
        return "Hodor"
      }
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
