<template>
  <div v-if="tagDistribution">
    <PieChart :chartData="tagDistribution" :options="chartConfig" :height="250" v-if="smallDataset"></PieChart>
  </div>
</template>

<script>
import PieChart from "@/components/charts/PieChart.js";

export default {
  mounted() {
    this.$store.dispatch("updateTagDistribution");
  },

  components: {
    // BarChart,
    // HBarChart,
    PieChart
  },

  computed: {
    tagColors() {
      if (this.$store.getters.tagDistribution) {
        // Get total labels
        let colorLen = this.$store.getters.tagDistribution.labels.length;

        // Return color array
        return Array(Math.floor(colorLen / 5) + 1)
          .fill(["#2D3142", "#4F5D75", "#BFC0C0", "#679436", "#EF8354"])
          .flat(colorLen);
      } else return ["#2D3142", "#4F5D75", "#BFC0C0", "#679436", "#EF8354"];
    },

    tagDistribution() {
      // Check chart data exists
      if (this.$store.getters.tagDistribution) {
        // Chart options and data
        let chartData = {
          labels: this.$store.getters.tagDistribution.labels,
          datasets: [
            {
              label: "Tag Distribution",
              data: this.$store.getters.tagDistribution.dataset,
              backgroundColor: this.tagColors,
              hoverWidth: 2,
              hoverColor: "#000"
            }
          ]
        };

        // Return processed data
        return chartData;
      } else return {};
    },

    smallDataset() {
      if (this.$store.getters.tagDistribution) {
        if (this.$store.getters.tagDistribution.labels.length > 5) {
          return false;
        } else return true;
      } else return null;
    }
  },

  data() {
    return {
      chartConfig: {
        maintainAspectRatio: true,
        reponsive: true,
        title: {
          display: false,
          text: "Extraction Method",
          fontSize: 25,
          fontColor: "#DC602E"
        },

        legend: {
          display: true,
          position: "bottom",
          maxWidth: 100,
          labels: {
            fontColor: "#1E152A",
            boxWidth: 20,
            fontSize: 12
          }
        }
        // scales: {
        //   xAxes: [
        //     {
        //       display: true,
        //       ticks: {
        //         fontSize: 12,
        //         suggestedMin: 0
        //       }
        //     }
        //   ],
        //   yAxes: [
        //     {
        //       ticks: {
        //         fontSize: 12,
        //         suggestedMin: 0
        //       }
        //     }
        //   ]
        // }

        // layout: {
        //   padding: {
        //       top: 50,
        //   },
        // }
      }
    };
  }
};
</script>

<style>
</style>