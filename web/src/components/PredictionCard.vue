<template>
  <div>

    <q-card>
      <q-card-section>
        <div class="text-caption text-grey-6">{{ subtitle }}</div>
        <div class="text-h6"> {{ title }}</div>
        <q-markup-table wrap-cells dense flat class="q-mt-lg">
          <tbody v-for="item in sentences" class="vertical-top">
          <tr>
            <td class="text-grey-8 text-right" v-if="item!=='??'">{{
                randomCharacter(item)
              }}
            </td>
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
const bbtChars = ["Leonard", "Sheldon", "Penny", "Howard", "Raj", "Bernadette", "Amy"];
const bbChars = ["Walter", "Skyler", "Jesse", "Marie", "Walter Jr", "Hank", "Saul", "Gus", "Mike"];
const hpChars = ["Harry", "Hermione", "Ron", "Draco", "Dobby", "Dumbledore", "Hagrid", "Ginny", "Snape", "Voldemort"];
const cmChars = ["Reid", "Garcia", "Jennifer", "Rossi", "Hotchner", "Morgan", "Prentiss", "Suspect 1", "Victim", "Suspect 2", "Lab Staff", "Guard", "Judge", "Witness"]

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
      if (String(item).includes('hodor')) {
        return "Hodor"
      }
      let chars;
      if (this.currentSerial === "got") {
        chars = gotChars;
      } else if (this.currentSerial === "bbt") {
        chars = bbtChars;
      } else if (this.currentSerial === "bb") {
        chars = bbChars;
      } else if (this.currentSerial === "hp") {
        chars = hpChars;
      } else if (this.currentSerial === "cm") {
        chars = cmChars;
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
