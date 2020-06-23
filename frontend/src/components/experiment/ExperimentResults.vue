<template>
  <div id="experiment-statistics" v-if="currentExperiment">
    <div class="chart-body">
      <bar-chart :chart-data="datacollection" :options="options" :height="325"></bar-chart>
    </div>
  </div>
</template>

<script>
import BarChart from "@/components/charts/BarChart.js";

export default {
  components: {
    BarChart
  },
  computed: {
    currentExperiment() {
      if (this.$store.getters.currentExperiment) {
        return this.$store.getters.currentExperiment;
      } else return null;
    },

    plotName() {
      return this.currentExperiment.name + " Amplification Count";
    },

    currentExperimentResults() {
      return this.$store.getters.currentExperimentResults;
    },

    currentSamples() {
      return this.$store.getters.currentSamples;
    },

    modificationSignal() {
      return this.$store.getters.modificationSignal;
    },

    uniqueLabels() {
      if (this.currentSamples) {
        const unique = [
          ...new Set(this.currentSamples.map(item => item.result))
        ];
        return unique;
      } else return null;
    },

    countResults() {
      if (this.uniqueLabels) {
        return this.uniqueLabels.map(result => {
          const filteredArray = this.currentSamples.filter(
            p => p.result == result
          );
          return Object.keys(filteredArray).length;
        });
      }
      return [0, 0, 0, 0];
    }
  },
  data() {
    return {
      colors: ["#969696", "#ef476f", "#26547c", "#ffd166", "#eff6ee"],
      datacollection: {},
      options: {}
    };
  },
  methods: {
    fillData() {
      const stats = this.currentExperimentResults.amp_status;
      this.datacollection = {
        labels: [this.currentExperiment.name],
        datasets: stats.map((result, i) => {
          return {
            label: result.marker,
            data: [result.sum],
            backgroundColor: this.colors[i]
          };
        })
      };
    },
    fillOptions() {
      this.options = {
        scales: {
          xAxes: [
            {
              display: false
            }
          ],
          yAxes: [
            {
              ticks: {
                beginAtZero: true
              }
            }
          ]
        },
        responsive: true,
        maintainAspectRatio: false,
        legend: {
          position: "bottom",
          // align: "center",
          labels: {
            boxWidth: 20,
            boxHeight: 10,
            padding: 15,
            fontSize: 12,
            usePointStyle: false
          }
        },
        title: {
          display: true,
          text: "Amplification Count",
          fontSize: 16
        }
      };
    }
  },
  watch: {
    modificationSignal() {
      this.fillData();
      this.fillOptions();
    },

    currentExperiment() {
      if (this.currentExperiment) {
        this.fillData();
        this.fillOptions();
      }
    },

    currentExperimentResults() {
      this.fillData();
      this.fillOptions();
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

#experiment-statistics {
  .chart-title {
    font-size: 1rem;
    font-weight: 400;
    margin-bottom: 8px;
    margin-top: 16px;
    text-align: center;
  }

  .details-values {
    color: $GreyDarker;
    font-weight: 500;
    font-size: 0.9rem;
  }

  .details-keys {
    color: $GreyDarker;
    font-weight: 400;
    font-size: 0.9rem;
  }

  .colors {
    background: #ac80a0;
    background: #ef476f;
    background: #ffd166;
    background: #26547c;
    background: #eff6ee;
  }
}
</style>