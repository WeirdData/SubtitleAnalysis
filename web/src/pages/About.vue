<template>
  <q-page padding class="justify-center q-pa-xl">
    <div class="row justify-center text-justify q-mb-lg">
      <p class="col-xs-12 col-md-5">
        With the help of this website, you can generate completely novel dialogues from your favourite
        serial with the help of Artificial Intelligence. You only have to provide the starting words and
        my neural network will complete the rest of the dialogue. Currently, these results are far from perfect
        but enjoy the art :) <br/>
        This project is part of bigger project called <a href="https://github.com/WeirdData/SubtitleAnalysis">SubtitleAnalysis</a>.
        It deals with various aspect of NLP and Text Generation algorithms. All neural networks used on this website
        were first trained on subtitles of following serials in python. Those models were then imported here
        to create the user interface. More technical details will be available on my Data-Science <a
        href="https://weirddata.github.io/" target="_blank">blog</a>.
        Following are some of the important points regarding these models,
        <q-list separator dense>
          <q-item></q-item>
          <q-item>Due to limitations in computational power, only a few 'epoch' were used for training of neural
            network.
          </q-item>
          <q-item>Game of Thrones model was only trained on subtitles from season 1</q-item>
          <q-item>Big Bang Theory, Criminal Minds, Breaking Bad models were trained on first 250000 characters</q-item>
          <q-item>Harry Potter series model includes subtitles from all 7 Harry Potter movies</q-item>
          <q-item>I will keep updating these models as I train them more with better parameters</q-item>
          <q-item></q-item>
        </q-list>

        All the home page posters were taken from IMDB. Website was designed by Rohit Suratekar. Full
        source-code can be found <a href="https://github.com/WeirdData/SubtitleAnalysis/tree/master/web"
                                    target="_blank"> here</a>. If you have an idea about this project, do
        share with me. You can contact me on <b>rohitsuratekar@protonmail.com</b>

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
