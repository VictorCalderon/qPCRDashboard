<template>
  <div>
    <b-form-row class="m-3 mt-3" v-if="currentExperiment">
      <b-col lg="3" md="4" sm="12" xs="12">
        <ExperimentDetails></ExperimentDetails>
      </b-col>
      <b-col lg="6" md="6" sm="12" xs="12">
        <AmplificationPlot></AmplificationPlot>
      </b-col>
      <b-col lg="3" md="6" sm="12" xs="12">
        <ExperimentSamples></ExperimentSamples>
      </b-col>
      <b-col lg="6" md="6" sm="12" xs="12">
        <PCAPlot></PCAPlot>
      </b-col>
      <b-col lg="6" md="6" sm="12" xs="12">
        <ExperimentResults></ExperimentResults>
      </b-col>
    </b-form-row>

    <b-form-row class="mt-5 justify-content-center">
      <b-col v-if="!currentExperiment" cols="8">
        <b-card class="text-center mt-3 rounded">
          <div
            class="rounded py-2"
          >You don't seem to be working on any experiments right now. Use the engine to search for experiments.</div>
          <b-row align-h="center" class="mt-3">
            <b-button variant="info" v-b-modal.search-experiments-modal>Search Experiment</b-button>
          </b-row>
        </b-card>
      </b-col>
    </b-form-row>
  </div>
</template>

<script>
import ExperimentResults from "@/components/experiment/ExperimentResults";
import ExperimentDetails from "@/components/experiment/ExperimentDetails";
import AmplificationPlot from "@/components/experiment/AmplificationPlot";
import PCAPlot from "@/components/experiment/PCAPlot";
import ExperimentSamples from "@/components/experiment/ExperimentSamples";

export default {
  components: {
    AmplificationPlot,
    PCAPlot,
    ExperimentSamples,
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