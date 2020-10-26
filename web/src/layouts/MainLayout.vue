<template>
  <q-layout view="hHh lpR fFf">

    <q-header elevated class="bg-primary text-white header-height">
      <q-toolbar class="vertical-middle full-height">
        <q-toolbar-title class="text-center">
          <q-btn no-caps flat label="Dialogue Generator" size="24px" to="/">
          </q-btn>
        </q-toolbar-title>
      </q-toolbar>
    </q-header>

    <q-page-container class="full-height">
      <router-view/>
    </q-page-container>

    <q-footer reveal>
      <q-toolbar class="justify-center vertical-middle">
        <p class="text-center absolute-center text-grey-3">
          Rohit Suratekar © 2020. Read More about this analysis
          <a href="https://weirddata.github.io/" target="_blank" class="text-red-3">  here</a>.
        </p>
      </q-toolbar>
    </q-footer>
  </q-layout>
</template>

<script>


export default {
  name: 'MainLayout',
  data() {
    return {
      leftDrawerOpen: false,
    }
  }
}
</script>

<style>
.header-height {
  height: 80px;
}
</style>
