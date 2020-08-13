<template>
  <div>
    <b-form-row class="mt-2" v-if="currentExperiment">
      <b-col lg="8" md="12" sm="12" xs="12">
        <b-card
          no-body
          class="card-height mb-2"
          header-bg-variant="dark"
          header-text-variant="white"
        >
          <b-tabs card pills justified>
            <b-tab title="Amplification Plot">
              <AmpPlot></AmpPlot>
            </b-tab>
            <b-tab title="Sample Clusters">
              <LatentSpaceClusters></LatentSpaceClusters>
            </b-tab>
            <!-- <b-tab title="Threshold Cycle KDE">
              <ThresholdKDE></ThresholdKDE>
            </b-tab>-->
          </b-tabs>
        </b-card>
      </b-col>
      <b-col lg="4" md="12" sm="12" xs="12">
        <SampleTable></SampleTable>
      </b-col>
    </b-form-row>

    <b-form-row class="mt-5 justify-content-center" v-show="!currentExperiment">
      <b-col cols="8">
        <b-card class="text-center rounded">
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
import SampleTable from "@/components/experiment2/SampleTable";
import LatentSpaceClusters from "@/components/experiment2/LatentSpaceClusters";

export default {
  components: {
    AmpPlot,
    LatentSpaceClusters,
    SampleTable,
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

<style lang="scss" scoped>
.card-height {
  height: 85vh;
}

@media (max-width: 480px) {
  .card-height {
    height: 65vh;
  }
}
</style>
