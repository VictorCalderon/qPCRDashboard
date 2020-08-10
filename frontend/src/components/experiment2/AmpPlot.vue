<template>
  <div style="height: 790px" class="mt-3">
    <b-form-row>
      <b-col cols="12">{{currentSample ? currentSample.name : 'All'}}</b-col>
      <b-col sm="12">
        <line-chart :chart-data="qPCRData" :options="qPCROptions" style="height: 70vh"></line-chart>
      </b-col>
    </b-form-row>
  </div>
</template>

<script>
import LineChart from "@/components/charts/LineChart.js";

export default {
  components: {
    LineChart
  },

  data() {
    return {
      qPCROptions: {
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
          yAxes: [{ ticks: { suggestedMax: 5, min: 0 } }],
          gridLines: {
            display: false
          },
        }
      }
    };
  },

  methods: {
    getColor() {
      // Background colors
      return ['#004E8970', '#AA998F70', '#368F8B70', '#1C373870', '#4D484770'];
    },
  },

  computed: {
    currentSample() {
      return this.$store.getters.currentSample;
    },

    currentExperimentFluorescences() {
      if (this.$store.getters.currentExperimentFluorescences) {
        return this.$store.getters.currentExperimentFluorescences 
      }

      return []
    },

    uniqueMarkers() {
      // Unique markers
      if (this.currentExperimentFluorescences) {
        return [...new Set(this.currentExperimentFluorescences.map(item => item.marker))]
      }
      else return []
    },

    colorMap() {
      // Marker color combination
      if (this.uniqueMarkers) {

        // Empty color map
        let colorMap = {};

        // Iterate over markers
        for (let idx = 0; idx < this.uniqueMarkers.length; idx++) {
          let marker = this.uniqueMarkers[idx];
          colorMap[marker] = this.getColor()[idx]
        }

        // Return filled colormap
        return colorMap
      }

      // Null
      else return null
    },

    qPCRData() {
      return {
        labels: [...Array(40).keys()].map(cycle => cycle + 1),
        datasets: [...this.currentExperimentFluorescences.map((fluorescence, i) => {

          // Custom Border Color
          let sampleCompare = this.currentSample ? fluorescence.result_id == this.currentSample.result_id : false;
          let customBorderColor = sampleCompare ? '#D64045' : this.colorMap[fluorescence.marker];
          let customOrder = sampleCompare ? 0 : 1;

          return {
            index: i,
            label: fluorescence.sample,
            data: fluorescence.data,
            fill: false,
            marker: fluorescence.marker,
            borderColor: customBorderColor,
            order: customOrder
          }
        })
        ]
      };
    }
  }
};
</script>

<style>
</style>