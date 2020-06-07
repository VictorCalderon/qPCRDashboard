<template>
  <div>
    <div class="amp-details">
      <div class="amp-details-body">
        <span class="amp-details-keys">&nbsp;Sample Clusterization:&nbsp;</span>
        <span class="amp-details-values">&nbsp;{{ currentProject.name }}&nbsp;</span>&nbsp;
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

  data() {
    return {
      datacollection: {},
      options: {},
      currentSampleID: null,
      xAxis: "ORF1ab",
      yAxis: "RNase P"
    };
  },

  watch: {
    currentProject() {
      this.fillChart();
    },

    currentProjectResults() {
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
    currentProject() {
      return this.$store.getters.currentProject;
    },

    currentSamples() {
      return this.$store.getters.currentSamples;
    },

    currentProjectResults() {
      return this.$store.getters.currentProjectResults;
    },

    labels() {
      if (this.currentProjectResults) {
        return this.currentProjectResults.samples;
      } else return [];
    },

    currentAxes() {
      if (this.currentProjectResults) {
        return [
          ...this.currentProjectResults.data[this.xAxis].map((x, i) => {
            return {
              x: x,
              y: this.currentProjectResults.data[this.yAxis][i]
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
          yAxes: [
            {
              scaleLabel: {
                display: true,
                labelString: this.xAxis
              }
            }
          ],
          xAxes: [
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