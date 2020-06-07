<template>
  <div v-if="currentProject">
    <div>
      <b-row>
        <b-col>
          <b-button
            class="mt-3 py-2"
            variant="outline-secondary"
            block
            size="sm"
            v-b-modal.edit-projects-modal
          >Edit</b-button>
        </b-col>
        <b-col>
          <b-button
            class="mt-3 py-2"
            variant="outline-secondary"
            block
            size="sm"
            @click="exportCurrentProject"
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
    currentProject() {
      if (this.$store.getters.currentProject) {
        return this.$store.getters.currentProject;
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

    loadProjects() {
      this.$store.dispatch("loadProjects");
    },

    async exportCurrentProject() {
      await this.$store.dispatch("exportCurrentProject");

      this.exportBtnLabel = "Downloading...";

      setTimeout(() => {
        // Check every half a second if currentProjectFile is there
        let file = this.$store.getters.currentProjectFile;

        if (file != null) {
          // Make a blob with it
          file = new Blob([this.$store.getters.currentProjectFile], {
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

    deleteCurrentProject() {
      this.$store.dispatch("deleteProject", this.currentProject.id);
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
