<template>
  <b-overlay :show="loadingMaxGrad">
    <b-form-row>
      <b-col sm="12" class>
        <scatter-chart :chart-data="chartData" :options="chartOptions" class="clusterplot-height"></scatter-chart>
      </b-col>
    </b-form-row>
  </b-overlay>
</template>

<script>
import ScatterChart from "@/components/charts/ScatterChart.js";

export default {
  components: {
    ScatterChart,
  },
  
  data() {
    return {
      cID: 0,
      groupedColors: {},
      colors: ["#009DDC", "#F26430", "#2A2D34", '#465362'],
      toggleLegend: true
    };
  },

  watch: {
    experimentMaxGrad() {
      this.cID = 0
    }
  },

  computed: {
    loadingMaxGrad() {
      return this.$store.getters.loadingMaxGrad
    },

    experimentMaxGrad() {
      if (this.$store.getters.experimentMaxGrad) {
        // Oh my god
        const filteredArray = this.$store.getters.experimentMaxGrad
          .filter(elem => { 
            return this.filteredTable
            .some(f => { 
              return f.result_id == elem.result_id }
            )
          }
        );

        return filteredArray
      }
      return []
    },

    filteredTable() {
      return this.$store.getters.filteredTable
    },

    currentExperiment() {
      return this.$store.getters.currentExperiment;
    },

    currentSample() {
      return this.$store.getters.currentSample;
    },

    markerColor() {
      return this.$store.getters.markerColor
    },

    chartData() {
        return {
          labels: ["Maximum Gradient Analysis"],
          datasets: [
            ...this.experimentMaxGrad.map(d => {
              // Check if current data belongs to anyone selected
              const isSelected = this.currentSample.find(s => s.result_id == d.result_id) ? true : false;

              // Add alpha to all samples if a sample is selected
              const alpha = isSelected ? '99' : '05'

              // Color selected sample differently
              const customColor = this.currentSample.length == 0 ? this.markerColor[d.marker] + '75' : this.markerColor[d.marker] + alpha;

              // Change selected sample size
              let customOrder = isSelected ? 0 : 1;
              let customSize = isSelected ? 15 : 7; 


              // Return prepared samples
              return {
                label: d['sample'] + ' - ' + d['marker'],
                data: [{ x: d['cycle'], y: d['maxgrad'] }],
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
        return this.currentSample.sample
      }
      else return ''
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
                labelString: 'MaxCycle'
              },
              ticks: {
                display: true,
                max: 40, min: 5
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
                labelString: 'MaxGrad'
              },
              ticks: {
                display: true,
                suggestedMax: 0.3, min: 0
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
  height: 80vh;
}

@media (max-width: 480px) {
  .clusterplot-height {
    height: 50vh;
  }
}
</style>