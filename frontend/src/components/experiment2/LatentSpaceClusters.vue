<template>
  <div>
    <b-form-row>
      <b-col>
        <scatter-chart :chart-data="chartData" :options="chartOptions" :height="255"></scatter-chart>
      </b-col>
    </b-form-row>
  </div>
</template>

<script>
import ScatterChart from "@/components/charts/ScatterChart.js";

export default {
  components: {
    ScatterChart
  },

  computed: {
    clusterData() {
      return this.$store.getters.LSCData;
    },

    chartData() {
      if (this.clusterData) {
        return {
          labels: ["Latent Space Clusters"],
          datasets: [
            ...this.clusterData.map(d => {
              return {
                label: d.label,
                data: [{ x: d.x, y: d.y }],
                pointRadius: 7,
                pointBackgroundColor: this.clusterColors[d.cluster]
              };
            })
          ]
        };
      } else return {};
    },

    chartOptions() {
      return {
        legend: {
          display: false,
          position: "bottom",
          align: "center",
          labels: {
            boxWidth: 12,
            boxHeight: 10,
            padding: 10,
            fontSize: 10,
            usePointStyle: true
          }
        },
        tooltips: {
          callbacks: {
            label: function(tooltipItem, data) {
              var label = data.datasets[tooltipItem.index];
              return label.label;
            }
          }
        },
        scales: {
          xAxes: [
            {
              scaleLabel: {
                display: false,
                labelString: this.xAxis
              },
              ticks: {
                display: false
              },
              gridLines: {
                display: false
              }
            }
          ],
          yAxes: [
            {
              scaleLabel: {
                display: false,
                labelString: this.yAxis
              },
              ticks: {
                display: false
              },
              gridLines: {
                display: false
              }
            }
          ]
        }
      };
    }
  },

  data() {
    return {
      clusterColors: ["#CD4631", "#81ADC8", "#086788"],
      toggleLegend: true
    };
  }
};
</script>

<style>
</style>