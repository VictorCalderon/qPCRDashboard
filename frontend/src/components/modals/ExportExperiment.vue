<template>
  <div>
    <b-modal
      id="export-experiments-modal"
      ref="export-experiments-modal"
      size="sm"
      hide-footer
      button-size="sm"
      title="Export Experiment"
      v-if="currentExperiment"
      centered
    >
      <!-- <b-row>
        <b-col>
          <b-alert v-model="showMessage" variant="info" class="text-center">{{ message }}</b-alert>
        </b-col>
      </b-row>
      <b-row>
        <b-col>
          <b-card
            class="text-center pt-2"
            :title="currentExperiment.name"
            v-if="currentExperimentResults"
          >
            <b-card-text>Total Samples: {{ totalSamples }}</b-card-text>
            <b-card-text v-for="(marker, i) in Object.keys(currentExperimentResults.data)" :key="i">
              <h5 class="my-0">{{ marker }}</h5>
              mean Cq: {{ sum(currentExperimentResults.data[marker]) / totalAmplified(marker) }}
            </b-card-text>
          </b-card>
        </b-col>
      </b-row>
      <hr />-->
      <b-container>
        <b-row>
          <b-col>
            <b-button @click="exportCurrentExperiment" variant="outline-info" block>Export</b-button>
          </b-col>
          <b-col>
            <b-button variant="outline-danger" @click="hideModal" block>Cancel</b-button>
          </b-col>
        </b-row>
      </b-container>
    </b-modal>
  </div>
</template>

<script>
import FileDownload from "js-file-download";
import axios from "axios";

export default {
  methods: {
    hideModal() {
      this.$refs["export-experiments-modal"].hide();
    },
    async exportCurrentExperiment() {
      axios
        .get(`api/v1/experiments/export/${this.currentExperiment.id}`)
        .then(res => {
          let file = res.data.file;

          if (file != null) {
            // Make a blob with it
            file = new Blob([file], {
              type: "text/plain"
            });

            // Download file
            FileDownload(file, this.$store.getters.exportFilename);
          }
        })

        .then(() => {
          this.hideModal();
        });
    }
  },

  computed: {
    currentExperiment() {
      return this.$store.getters.currentExperiment;
    }
  },

  data() {
    return {
      sep: null,
      showMessage: null,
      message: null
    };
  }
};
</script>

<style>
</style>