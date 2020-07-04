<template>
  <PieChart :chartData="chartData" :options="chartConfig" :height="200"></PieChart>
</template>

<script>
import PieChart from "@/components/charts/PieChart.js";

export default {
  components: {
    PieChart
  },
  data() {
    return {
      chartData: {
        labels: [
          "Maxwell - saliva",
          "Maxwell - UTM",
          "PCA3 - saliva",
          "PCA3 - UTM",
          "Other"
        ],
        datasets: [
          {
            label: "Population",
            data: [2000, 600, 400, 300, 100],
            backgroundColor: [
              "#69A2B0",
              "#FF9D70",
              "#659157",
              "#30323D",
              "#E05263"
            ],
            hoverWidth: 2,
            hoverColor: "#000"
          }
        ]
      },
      chartConfig: {
        maintainAspectRatio: true,
        reponsive: true,
        title: {
          display: false,
          text: "Método de Extracción",
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
        },

        // scales: {
        //     xAxes: [{
        //         ticks: {
        //             fontSize: 12
        //         }
        //     }]
        // },

        layout: {
          // padding: {
          //     top: 50,
          // },
        }
      }
    };
  }
};
</script>

<style>
</style>