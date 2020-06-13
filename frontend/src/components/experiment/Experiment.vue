<template>
  <div class="overflow-auto mt-3 py-2 mb-2 bg-light rounded">
    <div v-if="allExperiments">
      <b-row class align-h="center">
        <b-button
          variant="outline-secondary"
          v-for="experiment in recentExperiments"
          :key="experiment.id"
          @click="selectExperiment(experiment)"
          class="m-1"
          :pressed="currentExperiment.id == experiment.id"
        >
          <span>{{experiment.name | shortName }}</span>
        </b-button>
      </b-row>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      current: null,
      experimentListOffset: 0
    };
  },
  methods: {
    async selectExperiment(experiment) {
      await this.$store.dispatch("selectExperiment", experiment);
      await this.$store.dispatch("loadCurrentSamples");
      await this.$store.dispatch("loadExperimentFluorescences");
    }
  },
  computed: {
    allExperiments() {
      return this.$store.getters.allExperiments;
    },

    recentExperiments() {
      return this.$store.getters.recentExperiments;
    },

    currentExperiment() {
      if (this.$store.getters.currentExperiment == null) {
        return {};
      }
      return this.$store.getters.currentExperiment;
    }
  }
};
</script>
<style lang='scss' scoped>
$GreyDarker: #505050;
$Indicator: #34a0e9;

.experiments-header {
  color: $GreyDarker;
  font-size: 1.3rem;
  font-weight: 300;
  padding: 5px;
  font-weight: 300;
  margin: 0 10px 0 0px;
  padding: 10px 10px 6px 30px;
}

.no-experiments {
  text-align: center;
  font-size: 1.5rem;
  font-weight: 300;
  padding-top: 10px;
}

.upload-experiments {
  text-align: center;
  font-size: 1.3;
  font-weight: 300;
  padding-top: 10px;
}

.experiment-nav {
  display: block;
  padding: 1px 1px;
  margin-right: 20px;

  .page-button {
    font-size: 1.5rem;
    padding: 5px 0px;
    border-radius: 5px;
    border: none;
    background: none;
    cursor: pointer;

    .fas {
      color: $GreyDarker;
    }
    &:hover {
      background: $GreyDarker;
      color: white;

      .fas {
        color: white;
      }
    }

    &:disabled {
      &:hover {
        background: none;
        color: black;
      }

      .fas {
        color: black;
      }
    }
  }

  .experiment-list {
    display: grid;
    grid-template-columns: repeat(6, 1fr);

    .current {
      background: $GreyDarker;
      color: white;
    }
  }
  .experiment-item {
    background: none;
    text-align: center;
    color: black;
    padding: 10px 25px;
    border-radius: 5px;
    font-size: 0.9rem;
    font-weight: 400;
    border: 1px solid $GreyDarker;
    font-size: 300;
    margin: 0px 5px 5px 0px;

    &:hover {
      background: $GreyDarker;
      color: white;
      cursor: pointer;
    }
  }
}
</style>