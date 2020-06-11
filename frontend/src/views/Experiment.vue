<template>
    <div class="rounded" v-if="allExperiments">
      <div v-if="currentExperiment">
        <b-row class="mx-1 pt-1 mt-2 mb-1" align-h="center">
          <b-col cols="2" class="rounded mx-0">
            <ExperimentDetails></ExperimentDetails>
          </b-col>
          <b-col cols="6" class="rounded">
            <b-card>
              <Amplification></Amplification>
            </b-card>
          </b-col>
          <b-col cols="2" class="rounded">
            <b-card>
              <Samples></Samples>
            </b-card>
          </b-col>
        </b-row>
        <b-row class="mx-1 mt-2" align-h="center">
          <b-col cols="5" class="rounded">
            <b-card>
              <Clustering></Clustering>
            </b-card>
          </b-col>
          <b-col cols="5" class="rounded">
            <b-card>
              <ExperimentResults></ExperimentResults>
            </b-card>
          </b-col>
        </b-row>
      </div>
      <b-row v-else align-h="center">
        <b-card class="text-center mt-3 rounded">
          <div
            class="rounded py-2"
          >You don't seem to be working on any experiments right now. Use the engine to search for experiments.</div>
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
import ExperimentDetails from "@/components/experiment/ExperimentDetails";
import Amplification from "@/components/experiment/AmplificationPlot";
import Clustering from "@/components/experiment/ClusterPlot";
import Samples from "@/components/experiment/Samples";

export default {
  components: {
    Amplification,
    Clustering,
    Samples,
    ExperimentResults,
    ExperimentDetails
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