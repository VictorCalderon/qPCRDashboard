<template>
  <b-card
    bg-variant="light"
    align="center"
    header-bg-variant="dark"
    header-text-variant="white"
    class="m-2"
    v-if="currentExperimentResults"
  >
    <template v-slot:header>
      <b-row class="hue-selector" align-h="end">
        <b-col>
          <h5 class="mb-0 mt-1 thin-font">Principal Component Analysis</h5>
        </b-col>
        <b-col cols="5" class="my-0 py-0">
          <b-form-select
            v-model="marker"
            :options="availableMarkers"
            size="sm"
            v-b-tooltip.hover="'Color samples based on their amplification status'"
          ></b-form-select>
        </b-col>
      </b-row>
    </template>

    <b-form-row>
      <b-col>
        <scatter-chart :chart-data="scatterData" :options="options" :height="295" v-if="marker"></scatter-chart>
      </b-col>
    </b-form-row>
  </b-card>
</template>

<script>
import ScatterChart from "@/components/charts/ScatterChart.js";

export default {
  components: {
    ScatterChart
  },

  data() {
    return {
      scatterData: {},
      options: {},
      currentSampleID: null,
      xAxis: "PCA 1",
      yAxis: "PCA 2",
      marker: null,
      notAmped: "#ffffff50",
      amped: "#00000080"
    };
  },

  watch: {
    currentExperiment() {
      this.fillChart();
    },

    currentExperimentResults() {
      this.fillChart();
      this.marker = this.availableMarkers[0];
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
                display: false,
                labelString: this.xAxis
              }
            }
          ],
          yAxes: [
            {
              scaleLabel: {
                display: false,
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
  position: relative;
  margin: 0;
  font-size: 1rem;
  // margin-top: 15px;
  // margin-right: 0px;
  font-weight: 300;
  text-align: center;
}

.no-marker {
  font-size: 2rem;
  font-weight: 300;
  text-align: center;
  margin-top: 5%;
}
</style>