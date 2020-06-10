<template>
  <div>
    <div class="amp-details">
      <div class="amp-details-body">
        <span class="amp-details-keys">&nbsp;Sample Clusterization:&nbsp;</span>
        <span class="amp-details-values">&nbsp;{{ currentExperiment.name }}&nbsp;</span>&nbsp;
      </div>
    </div>
    <div class="chart-body">
      <scatter-chart :chart-data="datacollection" :options="options" :height="300"></scatter-chart>
    </div>
  </div>
</template>

<script>
import ScatterChart from "@/components/charts/ScatterChart.js";

export default {
  components: {
    ScatterChart
  },

  // [SUGGESTION] (Clusterplot.vue) xAxis and yAxis MUST be dynamic on mount
  data() {
    return {
      datacollection: {},
      options: {},
      currentSampleID: null,
      xAxis: "SARS-CoV-2 Gene",
      yAxis: "Internal Control"
    };
  },

  watch: {
    currentExperiment() {
      this.fillChart();
    },

    currentExperimentResults() {
      this.fillChart();
    },

    xAxis() {
      this.fillChart();
    },

    yAxis() {
      this.fillChart();
    }
  },

  computed: {
    currentExperiment() {
      return this.$store.getters.currentExperiment;
    },

    currentSamples() {
      return this.$store.getters.currentSamples;
    },

    currentExperimentResults() {
      return this.$store.getters.currentExperimentResults;
    },

    labels() {
      if (this.currentExperimentResults) {
        return this.currentExperimentResults.samples;
      } else return [];
    },

    currentMarkers() {
      if (this.currentExperimentResults) {
        return this.currentExperimentResults.statistics.map(p => {
          return p.marker;
        });
      } else return [];
    },

    currentAxes() {
      if (this.currentExperimentResults) {
        return [
          ...this.currentExperimentResults.data[this.xAxis].map((x, i) => {
            return {
              x: x,
              y: this.currentExperimentResults.data[this.yAxis][i]
            };
          })
        ];
      } else return [];
    }
  },

  methods: {
    fillChart() {
      this.fillData();
      this.changeSettings();
    },

    fillData() {
      this.datacollection = {
        labels: this.labels,
        datasets: [
          {
            data: this.currentAxes,
            pointRadius: 5,
            backgroundColor: "#34a0e9"
          }
        ]
      };
    },

    changeSettings() {
      this.options = {
        responsive: true,
        maintainAspectRatio: false,
        // onClick: function(evt, activeElements) {
        //   const sample_id = res.data.ids[activeElements[0]._index];
        //   this.$store.dispatch("selectSample", sample_id);
        //   this.update();
        // },
        tooltips: {
          callbacks: {
            label: function(tooltipItem, data) {
              var label = data.labels[tooltipItem.index];
              return (
                label +
                ": (" +
                tooltipItem.xLabel +
                ", " +
                tooltipItem.yLabel +
                ")"
              );
            }
          }
        },
        scales: {
          xAxes: [
            {
              scaleLabel: {
                display: true,
                labelString: this.xAxis
              }
            }
          ],
          yAxes: [
            {
              scaleLabel: {
                display: true,
                labelString: this.yAxis
              }
            }
          ]
        },
        legend: {
          display: false,
          position: "bottom",
          align: "center",
          labels: {
            boxWidth: 20,
            padding: 10
          }
        },
        title: {
          display: false,
          text: "ORF1ab Cycle vs RNase P Cycle",
          fontSize: 12
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

.chart-body {
  align-items: center;
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
</style>