<template>
  <PieChart :chartData="chartData" :options="chartConfig" :height="320"></PieChart>
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
          "Sede Central",
          "Naco",
          "Santiago",
          "La Vega",
          "Punta Cana",
          "Samaná",
          "San Juan",
          "Monte Cristi"
        ],
        datasets: [
          {
            label: "Samples analyzed",
            data: [3212, 1921, 1232, 989, 802, 702, 501, 339, 121, 0],
            backgroundColor: [
              "#DD614A",
              "#F48668",
              "#5AB1BB",
              "#A5C882",
              "#F7DD72",
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
        // scales: {
        //   xAxes: [
        //     {
        //       ticks: {
        //         fontSize: 12
        //       }
        //     }
        //   ]
        // },
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