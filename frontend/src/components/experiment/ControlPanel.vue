<template>
  <div v-if="currentExperiment">
    <div>
      <b-row>
        <b-col>
          <b-button
            class="mt-3 py-2"
            variant="outline-secondary"
            block
            size="sm"
            v-b-modal.edit-experiments-modal
          >Edit</b-button>
        </b-col>
        <b-col>
          <b-button
            class="mt-3 py-2"
            variant="outline-secondary"
            block
            size="sm"
            @click="exportCurrentExperiment"
          >Export</b-button>
        </b-col>
      </b-row>
    </div>
  </div>
</template>

<script>
import FileDownload from "js-file-download";

export default {
  computed: {
    currentExperiment() {
      if (this.$store.getters.currentExperiment) {
        return this.$store.getters.currentExperiment;
      } else return null;
    }
  },
  data() {
    return {
      deleteConfirmation: false,
      exportConfirmation: false,
      primaryOptions: true,
      exportBtnLabel: "Yes",
      deleteBtnLabel: "Yes"
    };
  },
  methods: {
    toggleDelete() {
      this.deleteConfirmation = !this.deleteConfirmation;
      this.primaryOptions = !this.primaryOptions;
    },

    toggleExport() {
      this.exportConfirmation = !this.exportConfirmation;
      this.primaryOptions = !this.primaryOptions;
    },

    loadExperiments() {
      this.$store.dispatch("loadExperiments");
    },

    async exportCurrentExperiment() {
      await this.$store.dispatch("exportCurrentExperiment");

      this.exportBtnLabel = "Downloading...";

      setTimeout(() => {
        // Check every half a second if currentExperimentFile is there
        let file = this.$store.getters.currentExperimentFile;

        if (file != null) {
          // Make a blob with it
          file = new Blob([this.$store.getters.currentExperimentFile], {
            type: "text/plain"
          });

          // Download file
          FileDownload(file, this.$store.getters.exportFilename);
        }
        this.exportBtnLabel = "Exported!";
        this.toggleExport();
        this.exportBtnLabel = "Yes";
      }, 1500);
    },

    deleteCurrentExperiment() {
      this.$store.dispatch("deleteExperiment", this.currentExperiment.id);
      this.deleteBtnLabel = "Deleted!";
      setTimeout(() => {
        this.toggleDelete();
        this.deleteBtnLabel = "Yes";
      }, 1500);
    }
  },
  watch: {}
};
</script>
