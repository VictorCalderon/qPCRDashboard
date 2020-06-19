<template>
  <div class="my-1 mx-0">
    <b-row align-h="center" class="my-1">
      <b-col>
        <div class="my-1 mx-0 px-0 text-center">
          <p class="my-auto hue-selector text-secondary">Principal Component Analysis</p>
          <b-button
            v-for="(m, i) in availableMarkers"
            :key="i"
            @click="setMarker(m)"
            class="m-md-1"
            :variant="marker == m ? 'secondary' : 'outline-secondary'"
          >{{ m }}</b-button>
        </div>
        <div>
          <scatter-chart :chart-data="scatterData" :options="options" :height="330" v-if="marker"></scatter-chart>
        </div>
      </b-col>
    </b-row>
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
      scatterData: {},
      options: {},
      currentSampleID: null,
      xAxis: "PCA 1",
      yAxis: "PCA 2",
      marker: null,
      notAmped: "#f1434350",
      amped: "#539ee480"
    };
  },

  watch: {
    currentExperiment() {
      this.fillChart();
    },

    currentExperimentResults() {
      this.fillChart();
      this.marker = null;
    },

    marker() {
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
    markerHue() {
      if (this.marker) {
        return `Current hue: ${this.marker}`;
      } else return "";
    },
    currentExperiment() {
      return this.$store.getters.currentExperiment;
    },

    currentSamples() {
      return this.$store.getters.currentSamples;
    },

    currentExperimentResults() {
      return this.$store.getters.currentExperimentResults;
    },

    availableMarkers() {
      if (this.currentExperimentResults) {
        return Object.keys(this.currentExperimentResults.amp_raw);
      } else return null;
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

    plotName() {
      return this.currentExperiment.name + " Cq Scatterplot";
    },

    currentAxes() {
      if (this.currentExperimentResults) {
        return [
          ...this.currentExperimentResults.cq_raw[this.xAxis].map((x, i) => {
            return {
              x: x,
              y: this.currentExperimentResults.cq_raw[this.yAxis][i]
            };
          })
        ];
      } else return [];
    },

    pointBackgroundColor() {
      if (this.currentExperimentResults) {
        let status = this.currentExperimentResults.amp_raw[this.marker];
        if (status) {
          return status.map(s => {
            return s ? this.amped : this.notAmped;
          });
        } else return null;
      } else return [];
    }
  },

  methods: {
    fillChart() {
      this.fillData();
      this.changeSettings();
    },

    setMarker(marker) {
      this.marker = marker;
    },

    fillData() {
      this.scatterData = {
        labels: this.labels,
        datasets: [
          {
            data: this.currentAxes,
            pointRadius: 5,
            pointBackgroundColor: this.pointBackgroundColor
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
          text: "Principal Component Analysis",
          fontSize: 16
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
$Somered: #f14343;

.chart-body {
  align-items: center;
}

.hue-selector {
  font-size: 1.2rem;
  font-weight: 400;
  text-align: center;
  padding-bottom: 6px;
}

.no-marker {
  font-size: 2rem;
  font-weight: 300;
  text-align: center;
  margin-top: 5%;
}
</style>