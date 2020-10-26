<template>
  <v-card>
    <v-img
        height="400"
        contain
        src="@/assets/serials/got.jpg"
    ></v-img>
  </v-card>
</template>

<script>
export default {
  name: "HomeCard",
  props: {
    id: String
  },
  methods: {
    getTitle: function () {
      switch (this.id) {
        case 'got':
          return "Game of Thrones";
        case 'bbt':
          return "Big Bang Theory";
        case 'bb' :
          return "Breaking Bad";
        default:
          return "Untitled"
      }
    }
  }
}
</script>

<style scoped>

</style>