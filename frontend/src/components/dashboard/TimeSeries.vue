<template>
  <b-container v-if="allExperiments">
    <b-row align-h="center" class="mt-5 mb-1">
      <h1 class="font-weight-light">Amplification Fraction Time Series</h1>
    </b-row>
    <b-row align-h="center" py-0>
      <b-col cols="3">
        <b-form-select v-model="marker" :options="options" class="mt-1"></b-form-select>
      </b-col>
    </b-row>
    <b-row class="m-5" align-h="center" v-if="marker">
      <LineChart
        :width="1300"
        :height="400"
        :chartData="chartData"
        :options="chartConfig"
        class="bg-light px-5 pt-5 pb-4"
      ></LineChart>
    </b-row>
  </b-container>
  <b-container v-else>
    <b-row align-h="center">
      <b-card class="text-center mt-5 rounded">
        <div
          class="rounded py-2"
        >You don't have any experiments. Add a new experiment and start analyzing your data.</div>
        <b-row align-h="center" class="mt-3">
          <b-button variant="info" v-b-modal.add-experiments-modal>Add Experiment</b-button>
        </b-row>
      </b-card>
    </b-row>
  </b-container>
</template>

<script>
import LineChart from "@/components/charts/LineChart.js";
// import palette from "@/components/dashboard/colors.js";
import axios from "axios";

export default {
  data() {
    return {
      marker: null,
      markersExists: null,
      options: [{ value: null, text: "Choose a marker" }],
      chartData: {},
      chartConfig: {
        scales: {
          xAxes: [{ display: true }],
          yAxes: [{ ticks: { suggestedMax: 0.5, suggestedMin: 0 } }]
        },
        responsive: true,
        maintainAspectRatio: false,
        tooltips: {
          // callbacks: {
          //   label: function(tooltipItem) {
          //     var label = this.data["Total Projects"][tooltipItem.index];
          //     return (
          //       label +
          //       ": (" +
          //       tooltipItem.xLabel +
          //       ", " +
          //       tooltipItem.yLabel +
          //       ")"
          //     );
          //   }
          // }
        },
        legend: {
          position: "bottom",
          align: "center",
          labels: {
            boxWidth: 20,
            boxHeight: 10,
            padding: 15,
            fontSize: 12,
            usePointStyle: false
          }
        }
      },
      data: null
    };
  },

  components: {
    LineChart
  },

  methods: {
    async getDashboardData() {
      if (this.marker) {
        await axios.get(`api/v1/timeseries/${this.marker}`).then(res => {
          this.data = res.data;
        });
      } else this.data = null;
    },

    async getMarkers() {
      await axios.get("api/v1/markers").then(res => {
        let markers = res.data.markers;
        if (markers.length > 0) {
          this.options = [
            ...markers.map(m => {
              return { value: m[0], text: m[1] };
            }),
            ...this.options
          ];
          this.marker = markers[1][0];
        } else {
          this.markers = null;
        }
      });
    },

    fillData() {
      if (this.data) {
        this.chartData = {
          labels: this.data["Date"],
          datasets: [
            {
              label: "Percentage of Amplification",
              data: this.data["Amp Fraction"],
              pointRadius: this.data["Total Experiments"].map(p => {
                return 2 * p + 5;
              }),
              fill: true,
              backgroundColor: "#D5606285",
              pointBackgroundColor: "#D5606255",
              borderColor: "#D5606255",
              pointHoverRadius: 20
            }
          ]
        };
      }
    },

    fillSettings() {
      this.chartConfig = {
        scales: {
          xAxes: [{ display: true }],
          yAxes: [{ ticks: { suggestedMax: 1.2, suggestedMin: 0 } }]
        },
        responsive: true,
        maintainAspectRatio: false,
        legend: {
          position: "bottom",
          align: "center",
          labels: {
            boxWidth: 20,
            boxHeight: 10,
            padding: 15,
            fontSize: 12,
            usePointStyle: false
          }
        },
        // title: {
        //   display: true,
        //   text: this.marker,
        //   fontsize: 16
        // }
      };
    }
  },

  mounted() {
    this.getMarkers();
  },
  computed: {
    allExperiments() {
      return this.$store.getters.allExperiments;
    }
  },

  watch: {
    async marker() {
      await this.getDashboardData();
      await this.fillData();
      await this.fillSettings();
    },

    async allExperiments() {
      await this.getDashboardData();
      await this.fillData();
      await this.fillSettings();
    }
  }
};
</script>

<style>
</style>