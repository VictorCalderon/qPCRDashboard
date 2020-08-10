<template>
  <LineChart
    :chartData="ampPercDatasets"
    :options="chartConfig"
    style="height:475px"
    v-if="ampPercDatasets"
  ></LineChart>
</template>

<script>
import LineChart from "@/components/charts/LineChart.js";

export default {
  mounted() {
    this.$store.dispatch("ampStatusTimeline");
  },

  components: {
    LineChart
  },

  computed: {
    ampPercDatasets() {
      // Check chart data exists
      if (this.$store.getters.ampPercData) {
        // Chart labels
        const chartDates = this.$store.getters.ampPercData.dates;

        // Chart data
        const chartRawData = this.$store.getters.ampPercData.datasets;

        // Add chart options to dataset
        let chartData = chartRawData.map((d, i) => {
          return {
            label: d.marker,
            data: d.data,
            backgroundColor: this.colors[i],
            fill: true,
            hoverWidth: 2,
            hoverColor: "#000",
            order: i + 1
          };
        });

        // Return processed data
        return { labels: chartDates, datasets: chartData };
      } else return {};
    }
  },

  data() {
    return {
      colors: ["#2E5266", "#6E8898", "#D3D0CB", "#E2C044"],
      chartConfig: {
        maintainAspectRatio: false,
        reponsive: true,
        tooltips: {
          callbacks: {
            label: function(tooltipItem, data) {
              var label = data.datasets[tooltipItem.datasetIndex].label || "";

              if (label) {
                label += ": ";
              }

              label += tooltipItem.yLabel + "%";
              return label;
            }
          }
        },

        legend: {
          display: true,
          position: "bottom",
          maxWidth: 100,
          labels: {
            boxWidth: 20,
            fontSize: 12
          }
        },

        layout: {
          // padding: {
          //     top: 50,
          // },
        },

        scales: {
          xAxes: [
            {
              display: true,
              ticks: {
                fontSize: 12
              }
            }
          ],
          yAxes: [
            {
              ticks: {
                fontSize: 12,
                // Include a dollar sign in the ticks
                callback: function(value) {
                  return value + "%";
                },
                suggestedMax: 100,
                suggestedMin: 0
              }
            }
          ]
        },

        elements: {
          point: {
            radius: 5
          }
        }
      }
    };
  }
};
</script>

<style>
</style>