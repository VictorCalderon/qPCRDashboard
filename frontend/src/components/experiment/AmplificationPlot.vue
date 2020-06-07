<template>
  <div>
    <div class="amp-details">
      <div class="amp-details-body">
        <span class="amp-details-keys">&nbsp;Sample Name:&nbsp;</span>
        <span class="amp-details-values">&nbsp;{{ currentSample.sample }}&nbsp;</span>&nbsp;|&nbsp;
        <span class="amp-details-keys">&nbsp;Well&nbsp;:</span>
        <span class="amp-details-values">&nbsp;{{ well }}&nbsp;</span>
        <ModifySample></ModifySample>
      </div>
    </div>
    <div class="chart-body" v-if="currentSample">
      <line-chart :chart-data="datacollection" :options="options" :height="300"></line-chart>
    </div>
    <div v-else>
      <div>
        <h1 class="no-sample" v-if="!currentProject">Select a project</h1>
        <h1 class="no-sample" v-else>Select a sample</h1>
      </div>
    </div>
  </div>
</template>

<script>
import LineChart from "@/components/charts/LineChart.js";
import ModifySample from "@/components/experiment/ModifySample.vue";

export default {
  components: {
    LineChart,
    ModifySample
  },
  created() {
    this.changeSettings();
  },
  data() {
    return {
      colors: ["#E14544", "#535353", "#34a0e9", "#E8B53C"],
      well: null,
      datacollection: {},
      options: {}
    };
  },
  computed: {
    currentSample() {
      return this.$store.getters.currentSample;
    },

    currentProject() {
      return this.$store.getters.currentProject;
    },

    qPCRData() {
      return this.$store.getters.currentSampleqPCRs;
    },

    projectqPCRs() {
      return this.$store.getters.projectqPCRs;
    }
  },
  watch: {
    qPCRData() {
      if (Object.keys(this.qPCRData).length) {
        this.fillData();
        this.well = this.qPCRData[0].well;
      }
    },
    currentProject() {
      if (Object.keys(this.qPCRData).length) {
        this.fillData();
        this.well = this.qPCRData[0].well;
      }
    }
  },
  methods: {
    fillData() {
      this.datacollection = {
        labels: [...Array(40).keys()].map(i => i + 1),
        datasets: [
          ...this.qPCRData.map((amp, index) => {
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
      };
    }
  }
};
</script>

<style lang='scss' scoped>
$GreyLight: #d8d8d8;
$GreyDark: #969696;
$GreenRef: #00843d;
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
