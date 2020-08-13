<template>
  <div class="card-height">
    <b-form-row>
      <b-col cols="12">{{currentSample ? currentSample.name : ''}}</b-col>
      <b-col sm="12">
        <line-chart :chart-data="qPCRData" :options="qPCROptions" class="ampplot-height"></line-chart>
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
     
    };
  },

  methods: {
    getColor() {
      // Background colors
      return ['#004E98', '#9C3848', '#FF6700', '#0A8754', '#1A281F'];
    },
  },

  computed: {
    currentSample() {
      return this.$store.getters.currentSample;
    },

    currentExperiment() {
      return this.$store.getters.currentExperiment
    },

    lineOpacity() {
      if (this.currentSample) {
        return '10'
      }

      else return '80'
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

    qPCROptions() {
      return {
        title: {
          display: true,
          text: this.currentExperiment.name,
          fontSize: 18,
          fontStyle: 'normal'
        },
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
        animation: true,
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
    },

    qPCRData() {
      return {
        labels: [...Array(40).keys()].map(cycle => cycle + 1),
        datasets: [...this.currentExperimentFluorescences.map((fluorescence, i) => {

          // Custom Border Color
          let sampleCompare = this.currentSample ? fluorescence.sample == this.currentSample.sample : false;
          let customBorderColor = sampleCompare ? this.colorMap[fluorescence.marker] : this.colorMap[fluorescence.marker] + this.lineOpacity;
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

<style lang='scss' scoped>
.ampplot-height {
  height: 75vh;
}

@media (max-width: 480px) {
  .ampplot-height {
    height: 50vh;
  }
}
</style>