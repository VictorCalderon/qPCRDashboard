<template>
  <b-card
    bg-variant="light"
    align="center"
    header-bg-variant="dark"
    header-text-variant="white"
    class="m-2"
  >
    <template v-slot:header>
      <b-form-row class="justify-content-end">
        <b-col cols="8">
          <h5 class="mb-0 thin-font">Experiment Samples</h5>
          <p class="my-0 smaller-font">Total: {{ totalSamples }}</p>
        </b-col>
        <b-col cols="2">
          <b-button size="sm" id="filter-popover" class="mt-2">
            <i class="fas fa-filter"></i>
          </b-button>
        </b-col>
      </b-form-row>

      <b-popover target="filter-popover" placement="bottom">
        <template v-slot:title>
          <b-form-input
            v-model="filter"
            placeholder="Filter samples"
            class="placeholder-light text-center bg-light borderless border-bottom"
          ></b-form-input>
        </template>
      </b-popover>
    </template>

    <div class="sample-list" :height="250">
      <b-row v-for="sample in filteredSamples" :key="sample.id" class="my-0 mt-0">
        <b-col>
          <b-button
            class="py-2 mt-1 border"
            :class="currentSample.sample == sample.sample ? 'bg-secondary text-light' : 'bg-light text-dark'"
            block
            @click="selectSample(sample.id)"
          >{{ sample.sample | shortName }}</b-button>
        </b-col>
      </b-row>
    </div>
  </b-card>
</template>

<script>
export default {
  data() {
    return {
      filter: null
    };
  },

  methods: {
    selectSample(id) {
      this.$store.dispatch("selectSample", id).then();
    }
  },

  computed: {
    currentSamples() {
      return this.$store.getters.currentSamples;
    },

    filteredSamples() {
      return this.$store.getters.filteredSamples;
    },

    searchFilter() {
      if (this.filter == "") return null;
      else return this.filter;
    },

    currentSample() {
      return this.$store.getters.currentSample;
    },

    currentExperimentResults() {
      return this.$store.getters.currentExperimentResults;
    },

    totalSamples() {
      if (this.currentExperimentResults) {
        return this.currentExperimentResults.samples.length;
      } else return 0;
    }
  },

  watch: {
    filteredSamples() {
      if (this.filteredSamples == null) return {};

      const firstSample = this.filteredSamples.slice(0, 1);
      this.selectSample(firstSample[0].id);
    },

    searchFilter() {
      this.$store.dispatch("filterSamples", this.filter);
    }
  }
};
</script>

<style lang='scss' scoped>
$GreyDarker: #505050;

.sample-list {
  height: 250px;
  width: 100%;
  overflow-y: scroll;
  -ms-overflow-style: none;

  &::-webkit-scrollbar {
    display: none;
  }

  -webkit-transition: all 0.1s ease-in-out;
  -moz-transition: all 0.1s ease-in-out;
  -ms-transition: all 0.1s ease-in-out;
  -o-transition: all 0.1s ease-in-out;
  transition: all 0.1s ease-in-out;
}

.no-projects {
  text-align: center;
  font-size: 1.2rem;
  font-weight: 500;
  padding-top: 100%;
}

.placeholder-light {
  ::placeholder {
    color: white !important;
  }
}
</style>