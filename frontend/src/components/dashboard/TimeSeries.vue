<template>
  <b-container>
    <b-row align-h="center" class="mt-5 mb-1">
      <h1 class="font-weight-light">Detected Ratio</h1>
    </b-row>
    <b-row align-h="center" py-0>
      <b-col cols="3">
        <b-form-select v-model="marker" :options="options" class="mt-1"></b-form-select>
      </b-col>
    </b-row>
    <b-row class="m-5" align-h="center" v-if="marker">
      <LineChart :width="1300" :height="500" :chartData="chartData" :options="chartConfig"></LineChart>
    </b-row>
  </b-container>
</template>

<script>
import LineChart from "@/components/charts/LineChart.js";
import Axios from "axios";

export default {
  data() {
    return {
      marker: null,
      options: [{ value: null, text: "Choose a marker" }],
      palette: [
        "#cc532f",
        "#45b2c4",
        "#d74164",
        "#57a95b",
        "#b05cc6",
        "#999a3e",
        "#7179cb",
        "#cc8b43",
        "#c46098",
        "#b9675d"
      ],
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
        await Axios.get(`api/v1/dashboard/${this.marker}`).then(res => {
          this.data = res.data;
        });
      } else this.data = null;
    },

    async getMarkers() {
      await Axios.get("api/v1/markers").then(res => {
        this.options = [...this.options, ...res.data.markers];
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
              pointRadius: this.data["Total Projects"].map(p => {
                return p + 5;
              }),
              fill: false,
              borderColor: this.palette,
              // pointRadius: 5,
              pointHoverRadius: 20
            }
            // {
            //   label: "Number of Projects",
            //   data: this.data["Total Projects"],
            //   pointRadius: this.data["Total Projects"],
            //   fill: false,
            //   borderColor: this.palette,
            //   // pointRadius: 5,
            //   pointHoverRadius: 8
            // }
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
        }
      };
    }
  },

  mounted() {
    this.getMarkers();
  },

  watch: {
    async marker() {
      await this.getDashboardData();
      await this.fillData();
    }
  }
};
</script>

<style>
</style>