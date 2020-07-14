<template>
  <div>
    <b-form-row class="justify-content-center mb-2">
      <b-col cols="4" class="my-0 py-0">
        <b-form-select v-model="marker" :options="availableMarkers" size="sm"></b-form-select>
      </b-col>
    </b-form-row>
    <b-form-row>
      <b-col>
        <line-chart :chart-data="qPCRData" :options="options" :height="255"></line-chart>
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
      marker: "ORF1ab",
      availableMarkers: ["ORF1ab", "RNase P"],
      options: {
        legend: {
          position: "bottom",
          align: "center",
          labels: {
            boxWidth: 12,
            boxHeight: 10,
            padding: 10,
            fontSize: 12,
            usePointStyle: false
          }
        }
      }
    };
  },

  methods: {
    sigmoid(t, ct) {
      return 1 / (1 + Math.exp(-(t - ct)));
    },

    generateAmpedDataset() {
      const ct = Math.random() * (30 - 18) + 18;
      return [...Array(40).keys()].map(i => this.sigmoid(i, ct) * 2.5);
    },

    generateNegativeDataset() {
      return [...Array(40).keys()].map(i => (i / i) * Math.random() * 0.15);
    }
  },

  computed: {
    qPCRData() {
      return {
        labels: [...Array(40).keys()].map(i => i + 1),
        datasets: [
          {
            label: "2001231232M1",
            data: this.generateAmpedDataset(),
            fill: false,
            borderColor: "#067BC2"
          },
          {
            label: "20012981212M1",
            data: this.generateAmpedDataset(),
            fill: false,
            borderColor: "#ECC30B"
          },
          {
            label: "20012981212M1",
            data: this.generateAmpedDataset(),
            fill: false,
            borderColor: "#F37748"
          },
          {
            label: "20012981212M1",
            data: this.generateNegativeDataset(),
            fill: false,
            borderColor: "#D56062"
          },
          {
            label: "20012981212M1",
            data: this.generateAmpedDataset(),
            fill: false,
            borderColor: "#2FBF71"
          },
          {
            label: "20012981212M1",
            data: this.generateAmpedDataset(),
            fill: false,
            borderColor: "#70D6FF"
          },
          {
            label: "20012981212M1",
            data: this.generateNegativeDataset(),
            fill: false,
            borderColor: "#FF70A6"
          }
        ]
      };
    }
  }
};
</script>

<style>
</style>