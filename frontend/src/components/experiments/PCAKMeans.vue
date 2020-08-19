<template>
  <div>
    <b-form-row class="justify-content-center">
      <!-- <b-col cols="12" class="text-center">{{ chartTitle }}</b-col> -->
      <b-col sm="12" v-if="!errorLoadingExperiment">
        <scatter-chart :chart-data="chartData" :options="chartOptions" class="clusterplot-height"></scatter-chart>
      </b-col>
      <b-col cols="8" sm="12" class="text-center border mt-5 py-5 rounded" v-else>
        <p class="text-center align-content-middle">
          Analysis resulted in error.
          <br />This could be due to duplicated samples or insufficient markers (at least 2).
        </p>
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
  
  data() {
    return {
      cID: 0,
      groupedColors: {},
      colors: ["#009DDC", "#F26430", "#2A2D34", '#465362'],
      groupColors: ["#2A2D34", "#009DDC", "#F26430"],
      toggleLegend: true
    };
  },

  watch: {
    experimentPCA() {
      this.cID = 0
    }
  },

  computed: {
    experimentPCA() {
      return this.$store.getters.experimentPCA ? this.$store.getters.experimentPCA : [];
    },

    errorLoadingExperiment() {
      return this.$store.getters.errorLoadingExperiment
    },

    currentExperiment() {
      return this.$store.getters.currentExperiment;
    },

    currentSample() {
      return this.$store.getters.currentSample;
    },

    chartData() {
        return {
          labels: ["Principal Component Analysis"],
          datasets: [
            ...this.experimentPCA.map(d => {

              // Color point
              if (!this.groupedColors[d.Cluster]) {
                  this.groupedColors[d.Cluster] = this.colors[this.cID]
                  this.cID += 1
              }

              // Check if current data belongs to anyone selected
              const isSelected = this.currentSample.find(s => s.sample == d.sample) ? true : false;

              // Add alpha to all samples if a sample is selected
              const alpha = isSelected ? '99' : '05'

              // Color selected sample differently
              const customColor = this.currentSample.length == 0 ? this.groupedColors[d.Cluster] + '75' : this.groupedColors[d.Cluster] + alpha;

              // Change selected sample size
              let customOrder = isSelected ? 0 : 1;
              let customSize = isSelected ? 15 : 7;

              return {
                label: d['sample'],
                data: [{ x: d['PCA 1'], y: d['PCA 2'] }],
                pointRadius: customSize,
                pointHoverRadius: 10,
                pointBackgroundColor: customColor,
                order: customOrder
              };
            })
          ]
      }
    },

    chartTitle() {
      if (this.currentSample) {
        return this.currentExperiment.name + ' | ' + this.currentSample.sample
      }
      else return this.currentExperiment.name
    },

    chartOptions() {
      return {
        animation: false,
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
        maintainAspectRatio: false,
        tooltips: {
          callbacks: {
            label: function(tooltipItem, data) {
              var sample = data.datasets[tooltipItem.datasetIndex];
              return sample.label;
            }
          }
        },
        scales: {
          xAxes: [
            {
              scaleLabel: {
                display: true,
                labelString: 'PCA 1'
              },
              ticks: {
                display: true
              },
              gridLines: {
                display: true
              }
            }
          ],
          yAxes: [
            {
              scaleLabel: {
                display: true,
                labelString: 'PCA 2'
              },
              ticks: {
                display: true
              },
              gridLines: {
                display: true
              }
            }
          ]
        }
      };
    }
  },
};
</script>


<style lang='scss' scoped>
.clusterplot-height {
  height: 72vh;
}

@media (max-width: 480px) {
  .clusterplot-height {
    height: 50vh;
  }
}
</style>