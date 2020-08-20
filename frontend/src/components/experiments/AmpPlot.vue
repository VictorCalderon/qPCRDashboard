<template>
  <b-overlay :show="loadingAmpPlot" variant="white" opacity="0.55" blur="1px" rounded="sm">
    <div class="card-height">
      <b-form-row>
        <b-col sm="12">
          <line-chart :chart-data="qPCRData" :options="qPCROptions" class="ampplot-height"></line-chart>
        </b-col>
      </b-form-row>
    </div>
  </b-overlay>
</template>

<script>
import LineChart from "@/components/charts/LineChart.js";

export default {
  components: {
    LineChart
  },

  data() {
    return {
      cID: 0,
      groupedColors: {},
      colors: ["#009DDC", "#F26430", "#FDB833", '#065143'],
    };
  },

  methods: {
  },

  watch: {
    qPCRData() {
      this.cID = 0
    }
  },

  computed: {
    currentSample() {
      return this.$store.getters.currentSample;
    },

    loadingAmpPlot() {
      return this.$store.getters.loadingAmpPlot
    },

    currentExperiment() {
      return this.$store.getters.currentExperiment
    },

    filteredTable() {
      return this.$store.getters.filteredTable
    },

    chartTitle() {
      if (this.currentSample) {
        return this.currentSample.sample
      }
      else return this.currentExperiment.name
    },

    availableMarkers() {
      if (this.currentExperimentFluorescences) {
        return new Set([...this.currentExperimentFluorescences.map(p => { return p.marker})])
      }
      else return []
    },

    currentExperimentFluorescences() {
      if (this.$store.getters.currentExperimentFluorescences) {
        // Oh my god
        const filteredArray = this.$store.getters.currentExperimentFluorescences
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

    qPCROptions() {
      return {
        normalized: true,
        spanGaps: true,
        elements: {
          point: { radius: 0 },
          line: {
            tension: 0, 
            fill: false,
            stepped: false,
            borderDash: []
          }
        },
        animation: false,
        tooltips: {
        enabled: true,
        callbacks: {
            label: function(tooltipItem, data) {
              let datapoint = data.datasets[tooltipItem.index];
              return datapoint.label;
            }
          }
        },
        maintainAspectRatio: false,
        legend: {
          display: false,
          position: "bottom",
          align: "center",
          labels: {
            boxWidth: 12,
            boxHeight: 10,
            padding: 10,
            fontSize: 10,
            usePointStyle: false
          }
        },
        scales: {
          xAxes: [
            {
              scaleLabel: {
                display: true,
                labelString: 'qPCR Cycles'
              },
              ticks: {
                display: true,
                max: 40, min: 10
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
                labelString: 'Fluorescence'
              },
              ticks: {
                display: true,
                suggestedMax: 2, min: 0
              },
              gridLines: {
                display: true
              }
            }
          ]
        }
      }
    },

    markerColor() {
      return this.$store.getters.markerColor
    },

    qPCRData() {
      return {
        labels: [...Array(40).keys()].map(cycle => cycle + 1),
        datasets: [...this.currentExperimentFluorescences.map((f, i) => {

          // Check if current data belongs to anyone selected
          const isSelected = this.currentSample.find(s => s.result_id == f.result_id) ? true : false

          // Add alpha to all samples if a sample is selected
          const alpha = isSelected ? '99' : '05'

          // Color selected sample differently
          const customBorderColor = this.currentSample.length == 0 ? this.markerColor[f.marker] + '75' : this.markerColor[f.marker] + alpha;

          // Bring selected sample to top
          const customOrder = isSelected ? 0 : 1;

          // Custom size
          const customSize = isSelected ? 1 : 0;

          return {
            index: i,
            label: f.sample,
            data: f.data,
            fill: false,
            marker: f.marker,
            borderColor: customBorderColor,
            borderSize: customSize,
            order: customOrder
          }
        })
        ]
      };
    }
  }
};
</script>

<style lang='scss' scoped>
.ampplot-height {
  height: 80vh;
}

@media (max-width: 480px) {
  .ampplot-height {
    height: 50vh;
  }
}
</style>