<template>
  <b-card
    bg-variant="light"
    align="center"
    header-bg-variant="dark"
    header-text-variant="white"
    class="m-2"
    v-if="currentSample"
  >
    <template v-slot:header>
      <h5 class="mb-0 thin-font">{{ currentSample.sample }}</h5>
      <p class="my-0 smaller-font">{{ well }}</p>
    </template>

    <b-form-row v-if="currentExperiment">
      <b-col>
        <line-chart :chart-data="datacollection" :options="options" :height="250"></line-chart>
      </b-col>
    </b-form-row>
  </b-card>
</template>

<script>
import LineChart from "@/components/charts/LineChart.js";

export default {
  components: {
    LineChart
  },

  created() {
    this.changeSettings();
  },

  data() {
    return {
      colors: ["#969696", "#ef476f", "#26547c", "#ffd166", "#eff6ee"],
      well: null,
      datacollection: {},
      options: {}
    };
  },
  computed: {
    currentSample() {
      return this.$store.getters.currentSample;
    },

    currentExperiment() {
      return this.$store.getters.currentExperiment;
    },

    fluorescenceData() {
      return this.$store.getters.currentSampleFluorescences;
    },

    experimentFluorescences() {
      return this.$store.getters.experimentFluorescences;
    },

    plotTitle() {
      return (
        "Sample Name: " + this.currentSample.sample + " | Well: " + this.well
      );
    }
  },

  watch: {
    fluorescenceData() {
      if (Object.keys(this.fluorescenceData).length) {
        this.fillData();
        this.well = this.fluorescenceData[0].well;
        this.changeSettings();
      }
    },

    currentExperiment() {
      if (Object.keys(this.fluorescenceData).length) {
        this.fillData();
        this.well = this.fluorescenceData[0].well;
        this.changeSettings();
      }
    },

    currentSample() {
      this.fillData();
      this.changeSettings();
    }
  },

  methods: {
    fillData() {
      this.datacollection = {
        labels: [...Array(40).keys()].map(i => i + 1),
        datasets: [
          ...this.fluorescenceData.map((amp, index) => {
            return {
              label: amp.marker,
              data: amp.amp,
              fill: false,
              borderColor: this.colors[index]
            };
          })
        ]
      };
    },

    changeSettings() {
      this.options = {
        scales: {
          xAxes: [{ display: true }],
          yAxes: [{ ticks: { suggestedMax: 2, suggestedMin: 0 } }]
        },
        responsive: true,
        maintainAspectRatio: false,
        legend: {
          position: "bottom",
          align: "center",
          labels: {
            boxWidth: 20,
            boxHeight: 10,
            padding: 15,
            fontSize: 12,
            usePointStyle: false
          }
        }
        // title: {
        //   display: true,
        //   text: "Sample Name: " + this.currentSample.sample + " | Well: " + this.well,
        //   fontSize: 16
        // }
      };
    }
  }
};
</script>

<style lang='scss' scoped>
$GreyLight: #d8d8d8;
$GreyDark: #969696;
$GreenRef: #a1a1a1;
$GreenRefDark: #005c2b;
$GreenRefLight: #01a34d;
$GreyDarker: #505050;
$GreyBackground: #e6e6e6;
$GreyBackgroundDark: #535353;
$Indicator: #539ee4;

.no-sample {
  text-align: center;
  font-size: 2.5rem;
  font-weight: 100;
  margin-top: 10%;
}

.amp-details {
  .settings-cog {
    position: absolute;
    right: 0px;
    top: -5px;
    color: $GreyDarker;
    font-size: 1rem;

    .fas {
      position: relative;
      top: 1px;
      font-size: 1.3rem;
    }
  }
  .amp-details-header {
    text-align: center;
    font-size: 1.2rem;
    font-weight: 300;
  }

  .amp-details-body {
    position: relative;
    top: 5px;
    text-align: center;
    margin: 9px;

    .amp-details-values {
      color: $GreyDarker;
      font-weight: 500;
      font-size: 0.9rem;
    }

    .amp-details-keys {
      color: $GreyDarker;
      font-weight: 400;
      font-size: 0.9rem;
    }

    .amp-details-sample {
      color: $GreyDarker;
      font-weight: 400;
      font-size: 1.2rem;
      // padding: 0px 10px;
      margin-bottom: 0px;
    }
  }
}

.chart-title {
  font-size: 1.8rem;
  font-weight: 300;
  margin-bottom: 20px;
  margin-top: 30px;
  text-align: center;
}

.chart-body {
  align-items: center;
  margin-top: 0%;
}

.chart-header {
  .result-picker {
    padding-top: 5px;
    margin: 5px;
    margin-left: 15%;
  }
}
</style>
