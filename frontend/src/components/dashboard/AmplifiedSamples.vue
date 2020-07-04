<template>
  <LineChart :chartData="chartData" :options="chartConfig" :height="200"></LineChart>
</template>

<script>
import LineChart from "@/components/charts/LineChart.js";

export default {
  components: {
    LineChart
  },
  data() {
    return {
      chartData: {
        labels: ["29 Jun", "30 Jun", "1 Jul", "2 Jul", "3 Jul"],
        datasets: [
          {
            label: "RNAse P",
            data: [100, 100, 100, 100, 100, 100, 0],
            backgroundColor: "#4C5454",
            fill: true,
            hoverWidth: 2,
            hoverColor: "#000",
            order: 3
          },
          {
            label: "ORF1ab",
            data: [25, 21, 20, 21, 20, 20, 0],
            backgroundColor: "#FF715B",
            fill: true,
            hoverWidth: 2,
            hoverColor: "#000",
            order: 2
          },
          {
            label: "E Gene",
            data: [19, 20, 18, 17, 23, 26, 0],
            backgroundColor: "#1EA896",
            fill: true,
            hoverWidth: 2,
            hoverColor: "#000",
            order: 1
          }
        ]
      },
      chartConfig: {
        maintainAspectRatio: true,
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
            // fontColor: "#05A8AA",
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
                suggestedMax: 30,
                suggestedMin: 0
              }
            }
          ]
        },

        elements: {
          point: {
            radius: 1
          }
        }
      }
    };
  }
};
</script>

<style>
</style>