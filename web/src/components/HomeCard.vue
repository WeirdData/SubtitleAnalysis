<template>
  <div class="test">
    <q-card>
      <q-img :src="getImage()">
        <div class="absolute-bottom text-subtitle2 text-center">
          {{ title }}
        </div>z
      </q-img>
    </q-card>
  </div>
</template>

<script>
export default {
  name: "HomeCard",
  props: ["title", "url", "img"],
  methods: {
    getImage: function () {
      return "images/" + this.img
    }
  }
}
</script>

<style scoped>

</style>
