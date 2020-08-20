<template>
  <BarChart
    :chartData="chartData"
    :options="chartConfig"
    class="locationcount-height"
    v-if="smallDataset"
  ></BarChart>
  <HBarChart :chartData="chartData" :options="chartConfig" class="locationcount-height" v-else></HBarChart>
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
              label: "Samples collected",
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
          display: true,
          position: "bottom",
          maxWidth: 100,
          labels: {
            fontColor: "#1E152A",
            boxWidth: 0,
            fontSize: 0
          }
        },

        layout: {
          // padding: {
          //     top: 50,
          // },
        },

        tooltips: {
        callbacks: {
          label: function(tooltipItem, data) {
            var label = data.datasets[tooltipItem.datasetIndex].label || "";

            if (label) {
              label += ": ";
            }

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
  height: 40vh;
}

@media (max-width: 480px) {
  .locationcount-height {
    height: 30vh;
  }
}
</style>