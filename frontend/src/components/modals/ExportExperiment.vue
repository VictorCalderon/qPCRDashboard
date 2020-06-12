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
      <b-container>
        <b-row class="my-1">
          <b-col>
            <div class="text-center">
              <label for="input-separator">Choose a separator</label>
              <b-form-select v-model="sep" :options="options" size="sm" class id="input-separator"></b-form-select>
            </div>
          </b-col>
        </b-row>
        <b-row class="mt-3">
          <b-col>
            <div class="text-center">
              <label for="select-columns">Select data to export</label>
              <b-button-group id="select-columns">
                <b-button variant="outline-secondary">Experiment</b-button>
                <b-button variant="outline-secondary">Date</b-button>
                <b-button variant="outline-secondary">Sample</b-button>
              </b-button-group>
            </div>
          </b-col>
        </b-row>
        <hr />
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
  data() {
    return {
      options: [
        { value: ",", text: "comma" },
        { value: "tab", text: "tab" }
      ],
      sep: ",",
      showMessage: null,
      message: null
    };
  },
  methods: {
    hideModal() {
      this.$refs["export-experiments-modal"].hide();
    },
    async exportCurrentExperiment() {
      const params = {
        sep: this.sep
      };
      axios
        .get(`api/v1/experiments/export/${this.currentExperiment.id}`, {
          params: params
        })
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
  }
};
</script>

<style>
</style>