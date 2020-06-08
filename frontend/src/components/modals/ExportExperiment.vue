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
      <b-row>
        <b-col>
          <b-alert v-model="showAlert" variant="info" class="text-center">{{ importMsg }}</b-alert>
        </b-col>
      </b-row>
      <b-row>
        <b-col>
          <b-card class="text-center pt-2" :sub-title="currentExperiment.name"></b-card>
        </b-col>
      </b-row>
      <hr />
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
export default {
  methods: {
    hideModal() {
      this.$refs["export-experiments-modal"].hide();
    },

    async exportCurrentExperiment() {
      // Dispatch export experiment
      await this.$store
        .dispatch("exportCurrentExperiment")
        .then(() => {
          let file = this.$store.getters.currentExperimentFile;
          if (file != null) {
            // Make a blob with it
            file = new Blob([this.$store.getters.currentExperimentFile], {
              type: "text/plain"
            });

            // Download file
            FileDownload(file, this.$store.getters.exportFilename);
          }
        })
        .then(() => {
          this.hideModal();
        });

      // // Set a timeout to check if the file is there
      // setTimeout(() => {
      //   // Check every half a second if currentExperimentFile is there
      //   let file = this.$store.getters.currentExperimentFile;

      //   if (file != null) {
      //     // Make a blob with it
      //     file = new Blob([this.$store.getters.currentExperimentFile], {
      //       type: "text/plain"
      //     });

      //     // Download file
      //     FileDownload(file, this.$store.getters.exportFilename);
      //   }
      // }, 1500);
    }
  },

  computed: {
    currentExperiment() {
      return this.$store.getters.currentExperiment;
    },

    experimentStats() {
      const stats = this.currentExperimentResults.statistics;
      return stats.map(result => {
        return {
          label: result.marker,
          data: [result.sum]
        };
      });
    }
  },

  data() {
    return {
      sep: null
    };
  }
};
</script>

<style>
</style>