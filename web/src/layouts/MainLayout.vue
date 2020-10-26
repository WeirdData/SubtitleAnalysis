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
