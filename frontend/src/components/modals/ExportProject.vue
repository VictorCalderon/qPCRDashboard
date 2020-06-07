<template>
  <div>
    <b-modal
      id="export-projects-modal"
      ref="export-projects-modal"
      size="sm"
      hide-footer
      button-size="sm"
      title="Export Project"
      v-if="currentProject"
      centered
    >
      <b-row>
        <b-col>
          <b-alert v-model="showAlert" variant="info" class="text-center">{{ importMsg }}</b-alert>
        </b-col>
      </b-row>
      <b-row>
        <b-col>
          <b-card class="text-center pt-2" :sub-title="currentProject.name"></b-card>
        </b-col>
      </b-row>
      <hr />
      <b-container>
        <b-row>
          <b-col>
            <b-button @click="exportCurrentProject" variant="outline-info" block>Export</b-button>
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
      this.$refs["export-projects-modal"].hide();
    },

    async exportCurrentProject() {
      // Dispatch export project
      await this.$store
        .dispatch("exportCurrentProject")
        .then(() => {
          let file = this.$store.getters.currentProjectFile;
          if (file != null) {
            // Make a blob with it
            file = new Blob([this.$store.getters.currentProjectFile], {
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
      //   // Check every half a second if currentProjectFile is there
      //   let file = this.$store.getters.currentProjectFile;

      //   if (file != null) {
      //     // Make a blob with it
      //     file = new Blob([this.$store.getters.currentProjectFile], {
      //       type: "text/plain"
      //     });

      //     // Download file
      //     FileDownload(file, this.$store.getters.exportFilename);
      //   }
      // }, 1500);
    }
  },

  computed: {
    currentProject() {
      return this.$store.getters.currentProject;
    },

    projectStats() {
      const stats = this.currentProjectResults.statistics;
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