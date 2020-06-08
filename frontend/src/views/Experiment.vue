<template>
  <div class="rounded" v-if="allExperiments">
    <!-- <Experiments></Experiments> -->
    <div v-if="currentExperiment">
      <b-row class="m-3" align-h="center">
        <b-col cols="2" class="bg-light rounded m-1">
          <Samples></Samples>
        </b-col>
        <b-col cols="8" class="bg-light rounded m-1">
          <Amplification></Amplification>
        </b-col>
        <b-col cols="5" class="bg-light rounded m-1">
          <Clustering></Clustering>
        </b-col>
        <b-col cols="5" class="bg-light rounded m-1">
          <ExperimentResults></ExperimentResults>
        </b-col>
      </b-row>
      <b-row class="m-5" align-h="center"></b-row>
    </div>
    <b-row v-else align-h="center">
      <b-card class="text-center mt-3 rounded">
        <div
          class="rounded py-2"
        >You don't have any opened experiments. Use the search engine or recent experiments bar.</div>
        <b-row align-h="center" class="mt-3">
          <b-button variant="info" v-b-modal.search-experiments-modal>Search Experiment</b-button>
        </b-row>
      </b-card>
    </b-row>
  </div>
  <div v-else>
    <b-row align-h="center">
      <b-card class="text-center mt-5 rounded">
        <div
          class="rounded py-2"
        >You don't have any experiments. Add a new experiment and start analyzing your data.</div>
        <b-row align-h="center" class="mt-3">
          <b-button variant="info" v-b-modal.add-experiments-modal>Add Experiment</b-button>
        </b-row>
      </b-card>
    </b-row>
  </div>
</template>

<script>
import ExperimentResults from "@/components/experiment/ExperimentResults";
import Amplification from "@/components/experiment/AmplificationPlot";
import Clustering from "@/components/experiment/ClusterPlot";
import Samples from "@/components/experiment/Samples";
// import Experiments from "@/components/experiment/Experiments";

export default {
  components: {
    Amplification,
    Clustering,
    Samples,
    ExperimentResults
    // Experiments
  },

  methods: {
    loadExperiments() {
      this.$store.dispatch("loadExperiments");
    }
  },

  computed: {
    currentExperiment() {
      return this.$store.getters.currentExperiment;
    },
    allExperiments() {
      return this.$store.getters.allExperiments;
    }
  },

  created() {
    this.loadExperiments();
  },

  data() {
    return {
      loading: false
    };
  }
};
</script>