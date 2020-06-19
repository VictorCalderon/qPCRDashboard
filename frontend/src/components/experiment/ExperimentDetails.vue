<template>
  <div class="text-center mt-1" v-if="currentExperimentResults">
    <div class="px-1 py-1 mb-1 rounded">
      <h4 class="thin-font">{{ currentExperiment.name}}</h4>
      <p class="my-0 smaller-font">Total Samples: {{ totalSamples }}</p>
    </div>
    <div class="overflow-results p-1" style="max-height: 300px">
      <div v-for="(marker, i) in markers" :key="i" class="bg-light mb-3 rounded py-2">
        <h5 class="my-0 rounded thin-font small-font">{{ marker }}</h5>
        <div>
          <p
            class="my-0 smaller-font"
          >Cq -> &nbsp;&mu;: {{ basicStatistics(marker).mean }} &nbsp;&nbsp; &sigma;: {{ basicStatistics(marker).std }}</p>
          <p class="my-0">Amp Percentage: &nbsp; {{ Math.round(basicStatistics(marker).perc, 2) }}%</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  methods: {
    basicStatistics(marker) {
      let markerStats = this.currentExperimentResults.amped_cq.filter(
        p => p.marker == marker
      )[0];

      let markerAmp = this.currentExperimentResults.amp_status.filter(
        p => p.marker == marker
      )[0];

      if (markerStats) {
        return {
          mean: Number(markerStats.mean.toFixed(2)),
          std: Number(markerStats.std.toFixed(2)),
          perc: Number(markerAmp.mean.toFixed(2)) * 100
        };
      } else {
        return {
          mean: 0.0,
          std: 0.0,
          perc: Number(markerAmp.mean.toFixed(2)) * 100
        };
      }
    }
  },
  computed: {
    currentExperiment() {
      return this.$store.getters.currentExperiment;
    },

    currentExperimentResults() {
      return this.$store.getters.currentExperimentResults;
    },

    totalSamples() {
      if (this.currentExperimentResults) {
        return this.currentExperimentResults.samples.length;
      } else return 0;
    },

    markers() {
      if (this.currentExperimentResults) {
        return this.currentExperimentResults.amp_status.map(p => {
          return p.marker;
        });
      } else return [];
    }
  },

  data() {
    return {
      sep: null,
      showMessage: null,
      message: null
    };
  }
};
</script>

<style>
.borderless {
  border: 0px !important;
}

.overflow-results {
  overflow-y: auto !important;
}

.thin-font {
  font-weight: 390 !important;
}

.small-font {
  font-size: 1rem !important;
}

.smaller-font {
  font-size: 0.9rem !important;
}
</style>