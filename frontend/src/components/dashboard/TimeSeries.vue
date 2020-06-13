<template>
  <b-container v-if="allExperiments">
    <b-row align-h="center" class="mt-5 mb-1">
      <h1 class="font-weight-light">Amplification Fraction Time Series</h1>
    </b-row>
    <b-row align-h="center" py-0>
      <b-col cols="3">
        <b-form-select v-model="marker" :options="options" class="mt-1 mr-1"></b-form-select>
      </b-col>
      <b-col cols="1">
        <b-button
          class="mt-1 ml-0 text-dark border"
          variant="outline-light"
          @click="downloadDataset"
          id='download-dataset'
        >
          <i class="fas fa-download"></i>
        </b-button>
        <b-tooltip target="download-dataset" triggers="hover" v-if="currentMarker" placement="right" variant="info">
          Download your dataset for <b>{{ currentMarker ? currentMarker : '' }}</b>
        </b-tooltip>
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
import axios from "axios";
import fileDownload from "js-file-download";

export default {
  data() {
    return {
      marker: null,
      markersExists: null,
      chartData: {},
      chartConfig: {},
      data: null,
      yAxis: "Amplification Fraction",
      file: null,
      rawMarkers: null
    };
  },

  components: {
    LineChart
  },

  methods: {
    async getTimeSeries() {
      if (this.marker) {
        let params = {
          marker_id: this.marker
        };
        await axios.get("api/v1/timeseries", { params: params }).then(res => {
          this.data = res.data;
        });
      } else this.data = null;
    },

    async downloadDataset() {
      if (this.marker) {
        let params = {
          marker_id: this.marker
        };

        await axios.get("api/v1/dataset", { params: params }).then(res => {
          let file = res.data.file;

          if (file != null) {
            
            // Create a blob
            file = new Blob([file], {
              type: "text/plain"
            });

            // Download file
            fileDownload(file, `qPCR-dataset-${this.currentMarker}.csv`);
          }
        });
      }
    },

    async getMarkers() {
      await this.$store.dispatch('getMarkers')
    },

    fillData() {
      if (this.data) {
        this.chartData = {
          labels: this.data["Date"],
          datasets: [
            {
              label: this.currentMarker,
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
          yAxes: [
            // { scaleLabel: { display: false, labelString: this.yAxis } },
            { ticks: { suggestedMax: 0.5, suggestedMin: 0 } }
          ]
        },
        responsive: true,
        maintainAspectRatio: false,
        tooltips: {},
        legend: {
          position: "bottom"

        }
      };
    }
  },

  beforeCreate() {
    this.$store.dispatch('getMarkers');
  },

  computed: {
    allExperiments() {
      return this.$store.getters.allExperiments;
    },

    markers() {
      return this.$store.getters.availableMarkers;
    },

    currentMarker() {
      if (this.markers && this.marker) {
        return this.markers.filter(marker => marker.value == this.marker)[0].text;
      }
      else return ''
    },

    options() {
      if (this.markers) {
        return [{ value: null, text: "Choose a marker" }, ...this.markers]
      }
      else return [{ value: null, text: "Choose a marker" }]
    }
  },

  watch: {
    async marker() {
      await this.getTimeSeries();
      await this.fillData();
      await this.fillSettings();
    },

    async allExperiments() {
      await this.getTimeSeries();
      await this.fillData();
      await this.fillSettings();
    }
  }
};
</script>

<style>
</style>