<template>
  <div id="experiment-statistics" v-if="currentExperiment">
    <h3 class="chart-title">
      <span class="details-values">Experiment:</span>&nbsp;
      <span class="details-keys">{{ currentExperiment.name }}</span>&nbsp;|
      <span class="details-keys">&nbsp;Status:&nbsp;</span>
      <span class="details-values">{{ currentExperiment.analyzed ? 'Analyzed' : 'Pending' }}&nbsp;</span>
    </h3>
    <div class="chart-body">
      <bar-chart :chart-data="datacollection" :options="options" :height="300"></bar-chart>
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
      colors: ["#E14544", "#535353", "#003a3ac0"],
      datacollection: {},
      options: {
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
        }
      }
    };
  },
  methods: {
    fillData() {
      const stats = this.currentExperimentResults.statistics;
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
    }
  },
  watch: {
    modificationSignal() {
      this.fillData();
    },

    currentExperiment() {
      if (this.currentExperiment) this.fillData();
    },

    currentExperimentResults() {
      this.fillData();
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
}
</style>