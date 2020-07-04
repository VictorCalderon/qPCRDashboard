<template>
  <BarChart :chartData="chartData" :options="chartConfig" :height="200"></BarChart>
</template>

<script>
import BarChart from "@/components/charts/BarChart.js";

export default {
  components: {
    BarChart
  },
  data() {
    return {
      chartData: {
        labels: ["Sede Central", "Naco", "Santiago", "La Vega", "Punta Cana"],
        datasets: [
          {
            label: "Muestras Procesadas",
            data: [3212, 1232, 1921, 802, 989, 0],
            backgroundColor: [
              "#DD614A",
              "#F48668",
              "#5AB1BB",
              "#A5C882",
              "#F7DD72"
            ],
            hoverWidth: 2,
            hoverColor: "#000"
          }
        ]
      },
      chartConfig: {
        scales: {
          xAxes: [
            {
              ticks: {
                fontSize: 12
              }
            }
          ]
        },
        maintainAspectRatio: true,
        reponsive: true,
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
        }
      }
    };
  }
};
</script>

<style>
</style>