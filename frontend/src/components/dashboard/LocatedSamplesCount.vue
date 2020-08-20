<template>
  <b-form-row>
    <b-col cols="12" v-if="smallDataset">
      <BarChart :chartData="chartData" :options="chartConfig" class="locationcount-height"></BarChart>
    </b-col>
    <b-col cols="12" v-else>
      <HBarChart :chartData="chartData" :options="chartConfig" class="locationcount-height"></HBarChart>
    </b-col>
  </b-form-row>
</template>

<script>
import BarChart from "@/components/charts/BarChart.js";
import HBarChart from "@/components/charts/HBarChart.js";

export default {
  components: {
    BarChart,
    HBarChart
  },

  computed: {
    smallDataset() {
      if (this.$store.getters.samplingSites) {
        if (this.$store.getters.samplingSites.length > 5) {
          return false;
        } else return true;
      } else return null;
    },

    samplingLabels() {
      return this.$store.getters.samplingSites.map(p => {
        return p.name;
      });
    },

    samplingDatasets() {
      return this.$store.getters.samplingSites.map(p => {
        return p.count;
      });
    },

    samplingColors() {
      return this.$store.getters.samplingSites.map(p => {
        return p.bgColor;
      });
    },

    samplingSites() {
      return this.$store.getters.samplingSites;
    },

    chartData() {
      if (this.samplingSites) {
        return {
          labels: this.samplingLabels,
          datasets: [
            {
              label: "Collected",
              data: this.samplingDatasets.map(c => {return Math.log(c)}),  // Log scaled plot
              backgroundColor: this.samplingColors,
              hoverWidth: 2,
              hoverColor: "#000"
            }
          ]
        };
      } else return {};
    }
  },

  data() {
    return {
      chartConfig: {
        maintainAspectRatio: false,
        reponsive: true,
        legend: {
          display: false,
          position: "bottom",
          labels: {
            fontColor: "#1E152A",
            boxWidth: 0,
            fontSize: 0
          }
        },
        yAxes: [
          {
            scaleLabel: {
              display: false,
            },
            ticks: {
              display: false,
            },
            gridLines: {
              display: true
            }
          }
        ],
        tooltips: {
          callbacks: {
            label: function(tooltipItem, data) {
              let label = data.datasets[tooltipItem.datasetIndex].label || "";
              if (label) { label += ": " }
              label += Math.exp(tooltipItem.yLabel);
              return label;
            }
          }
        },
      }
    };
  }
};
</script>

<style lang='scss' scoped>
.locationcount-height {
  height: 37vh;
}

@media (max-width: 480px) {
  .locationcount-height {
    height: 35vh;
  }
}
</style>