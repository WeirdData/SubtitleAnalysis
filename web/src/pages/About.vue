<template>
  <q-page padding class="justify-center q-pa-xl">
    <div class="row justify-center text-justify q-mb-lg">
      <p class="col-xs-12 col-md-5">
        Simple idea is to make a platform where one can generate artificial screenplay for the entire TV serial. Where the
        user can tell how they want the dialogue to start and Artificial Intelligence model will complete the rest of the conversation. It will
        provide enough space for both creativity as well as <a href="https://en.wikipedia.org/wiki/Natural_language_processing" target="_blank">NLP</a> implementation. Currently, these results are far from perfect
        but enjoy the art :) For more information, please check my Data-Science <a
        href="https://weirddata.github.io/2020/10/16/text-generation.html" target="_blank">blog</a>.
        Following are some of the important points regarding NLP models used in this website,
        <q-list separator dense>
          <q-item></q-item>
          <q-item>Game of Thrones model was only trained on subtitles from season 1</q-item>
          <q-item>Big Bang Theory, Criminal Minds, Breaking Bad models were trained on first 250000 characters</q-item>
          <q-item>Harry Potter series model includes subtitles from all 7 Harry Potter movies</q-item>
          <q-item>I will keep updating these models as I train them more with better parameters</q-item>
          <q-item></q-item>
        </q-list>

        All the home page posters were taken from IMDB. Website was designed by Rohit Suratekar. Full
        source-code can be found <a href="https://github.com/WeirdData/SubtitleAnalysis/tree/master/web"
                                    target="_blank"> here</a>. If you have an idea regarding this project, or
        want me to add your favorite TV serial here, do
        contact with me. You can reach me on <b>rohitsuratekar@protonmail.com</b>

      </p>
    </div>
    <q-footer>
      <q-toolbar class="justify-center vertical-middle">
        <p class="text-center absolute-center text-grey-3">
          Rohit Suratekar © 2020
        </p>
      </q-toolbar>
    </q-footer>
  </q-page>
</template>

<script>
export default {
  name: "About"
}
</script>

<style scoped>

</style>
