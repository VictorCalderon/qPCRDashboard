<template>
  <DoughnutChart :chartData="chartData" :options="chartConfig" :height="200"></DoughnutChart>
</template>

<script>
import DoughnutChart from "@/components/charts/DoughnutChart.js";

export default {
  components: {
    DoughnutChart
  },
  data() {
    return {
      chartData: {
        labels: ["Reportados", "Pendientes"],
        datasets: [
          {
            label: "Proyectos",
            data: [5, 3],
            backgroundColor: ["#4F772D", "#90A955"],
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
          fontColor: "#1E152A"
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

        layout: {
          // padding: {
          //     top: 50,
          // },
        },

        scales: {
          // xAxes: [{
          //     display: true, ticks: {
          //         fontSize: 12
          //     }
          // }],
          // yAxes: [{
          //     ticks: {
          //         // Include a dollar sign in the ticks
          //         callback: function (value, index, values) {
          //             return value + '%';
          //         },
          //         suggestedMax: 30,
          //         suggestedMin: 0
          //     }
          // }]
        }
      }
    };
  }
};
</script>

<style>
</style>