<template>
  <div>
    <b-form-row class="m-3 mt-3" v-if="currentExperiment">
      <b-col lg="8" md="12" sm="12" xs="12">
        <b-card no-body class="m-2" header-bg-variant="dark" header-text-variant="white">
          <b-tabs card fill pills>
            <b-tab title="Amplification Plot">
              <AmpPlot></AmpPlot>
            </b-tab>
            <b-tab title="Latent Space Clusters">
              <AEPlot></AEPlot>
              <h5>Latent Space Clusterization</h5>
            </b-tab>
            <b-tab title="Cycle Kernel Density">
              <CqDistribution></CqDistribution>
            </b-tab>
            <b-tab title="Observation Cloud">
              <ObservationCloud></ObservationCloud>
            </b-tab>
          </b-tabs>
        </b-card>
      </b-col>
      <b-col lg="4" md="12" sm="12" xs="12">
        <SampleTable></SampleTable>
      </b-col>
      <!-- <b-col lg="3" md="6" sm="12" xs="12">
        <SamplePlate></SamplePlate>
      </b-col>
      <b-col lg="6" md="6" sm="12" xs="12">
        <AEPlot></AEPlot>
      </b-col>
      <b-col lg="6" md="6" sm="12" xs="12">
        <CqBoxPlot></CqBoxPlot>
      </b-col>-->
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
import AmpPlot from "@/components/experiment2/AmpPlot";
// import SamplePlate from "@/components/experiment2/SamplePlate";
import SampleTable from "@/components/experiment2/SampleTable";
import ObservationCloud from "@/components/experiment2/ObservationCloud";
import CqDistribution from "@/components/experiment2/CqDistribution";

// import AEPlot from "@/components/experiment2/AEPlot";
// import CqBoxPlot from "@/components/experiment2/CqBoxPlot";

export default {
  components: {
    AmpPlot,
    // AEPlot,
    // SamplePlate,
    // CqBoxPlot,
    SampleTable,
    ObservationCloud,
    CqDistribution
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
