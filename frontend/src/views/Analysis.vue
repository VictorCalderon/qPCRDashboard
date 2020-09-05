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
            <b-tab lazy>
              <template v-slot:title>
                <span class="full-text">Amplification Plot</span>
                <span class="short-text">AmpPlot</span>
              </template>
              <AmpPlot></AmpPlot>
            </b-tab>
            <b-tab lazy>
              <template v-slot:title>
                <span class="full-text">PCA Clusterization</span>
                <span class="short-text">PCAClust</span>
              </template>
              <PCAKMeans></PCAKMeans>
            </b-tab>
            <b-tab lazy>
              <template v-slot:title>
                <span class="full-text">Maximum Gradient</span>
                <span class="short-text">MaxGrad</span>
              </template>
              <MaxGrad></MaxGrad>
            </b-tab>
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
            <b-button variant="info" v-b-modal.search-experiments-modal>Search Experiment Data</b-button>
          </b-row>
        </b-card>
      </b-col>
    </b-form-row>
  </div>
</template>

<script>
import AmpPlot from "@/components/analysis/AmpPlot";
import SampleTable from "@/components/analysis/SampleTable";
import PCAKMeans from "@/components/analysis/PCAKMeans";
import MaxGrad from "@/components/analysis/MaxGrad";

export default {
  components: {
    AmpPlot,
    PCAKMeans,
    SampleTable,
    MaxGrad
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
    },

    loadingAmpPlot() {
      return this.$store.getters.loadingAmpPlot
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
// Normal card height on fullscreen
.card-height {
  height: 90vh;
}

// Hide short text by default (resolution > 1200px)
.short-text {
  display: none;
}

// When resolution <= 1200px, hide full text and show short text
@media (max-width: 1200px) {
  .short-text {
    display: inline-block;
  }
  .full-text {
    display: none;
  }
}

@media (max-width: 480px) {
  .card-height {
    height: 65vh;
  }
}
</style>
