<template>
  <div>
    <v-row align="center" justify="center" class="ma-4">
      <v-col cols="5">
        <HomeCard id="got" />
      </v-col>
    </v-row>
  </div>
</template>

<script>
// @ is an alias to /src

import HomeCard from "@/components/HomeCard";

export default {
  name: 'Home',
  components: {HomeCard},
}
</script>
