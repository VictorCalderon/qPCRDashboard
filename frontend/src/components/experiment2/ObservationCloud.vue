<template>
  <b-form-row>
    <vue-word-cloud
      :words="words"
      :color="([, weight]) => weight > 10 ? '#F37748' : '#067BC2'"
      font-family="Roboto"
      style="height: 80vh;width: 1200px;"
      :animation-duration="500"
      :font-size-ratio="4"
      :spacing="0.2"
    />
  </b-form-row>
</template>

<script>
import VueWordCloud from "vuewordcloud";

export default {
  components: {
    [VueWordCloud.name]: VueWordCloud
  },

  methods: {
    wordClickHandler(name, value, vm) {
      console.log("wordClickHandler", name, value, vm);
    }
  },
  data() {
    return {
      myColors: ["#1f77b4", "#629fc9", "#94bedb", "#c9e0ef"],
      words: [
        ["cough", 26],
        ["fever", 19],
        ["dyspnea", 18],
        ["sore-throat", 16],
        ["diarrhoea", 12],
        ["tiredness", 10],
        ["loss-of-taste", 10],
        ["headache", 9],
        ["nausea", 7]
      ]
    };
  },

  computed: {
    wordColor() {
      return this.words.map(([, weight]) =>
        weight > 10 ? "#F37748" : "#067BC2"
      );
    }
  }
};
</script>

<style>
</style>