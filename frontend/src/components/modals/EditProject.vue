<template>
  <b-modal
    id="edit-projects-modal"
    ref="edit-projects-modal"
    class="text-center"
    title="Edit Project"
    size="md"
    centered
    hide-footer
    scrollable
  >
    <b-container v-if="currentProject">
      <b-alert v-model="showAlert" variant="info" class="text-center">{{ updateMsg }}</b-alert>
      <b-row class="mb-2">
        <b-col>
          <div class="text-center">
            <label for="edit-projectname">Type name</label>
            <b-form-input
              id="edit-projectname"
              v-model="project.name"
              class="text-center"
              :placeholder="currentProject.name"
            ></b-form-input>
          </div>
        </b-col>
        <b-col>
          <div class="text-center">
            <label for="edit-datepicker">Choose a date</label>
            <b-form-datepicker
              id="edit-datepicker"
              v-model="project.experiment_date"
              class="mb-2"
              locale="en"
              :date-format-options="{ year: 'numeric', month: 'short', day: '2-digit' }"
              :placeholder="currentProject.experiment_date"
            ></b-form-datepicker>
          </div>
        </b-col>
      </b-row>
      <hr />
      <b-row class="mb-2" align-h="center">
        <b-col>
          <div class="text-center">
            <label for="edit-projectname">Descriptions and Observations</label>
            <b-form-textarea
              id="edit-projectname"
              v-model="project.observations"
              class="text-center"
              :placeholder="currentProject.observations"
            ></b-form-textarea>
          </div>
        </b-col>
      </b-row>
      <b-row>
        <b-col cols="10" offset="1">
          <hr />
          <div class="text-center">
            <b-form-group label="Project status">
              <b-row class="mt-2">
                <b-col>
                  <b-form-radio
                    v-model="project.analyzed"
                    name="analyzed-radios"
                    value="true"
                  >Analyzed</b-form-radio>
                </b-col>
                <b-col>
                  <b-form-radio
                    v-model="project.analyzed"
                    name="analyzed-radios"
                    value="false"
                  >Pending</b-form-radio>
                </b-col>
              </b-row>
              <hr />
              <b-row class="mt-1">
                <b-col>
                  <label for="delete-project-button">Delete current project</label>
                  <b-button
                    id="delete-project-button"
                    size="md"
                    variant="outline-danger"
                    @click="deleteCurrentProject"
                    block
                  >Delete</b-button>
                </b-col>
              </b-row>
              <hr />
            </b-form-group>
          </div>
        </b-col>
      </b-row>
      <b-row>
        <b-col>
          <b-button
            id="update-project-button"
            size="md"
            variant="success"
            @click="modifyProject"
            block
          >Update</b-button>
        </b-col>
        <b-col>
          <b-button
            id="cancel-project-button"
            size="md"
            variant="warning"
            @click="hideModal"
            block
          >Cancel</b-button>
        </b-col>
      </b-row>
    </b-container>
    <b-container v-else>
      <b-row align-h="center">
        <h5 class="my-2">Please open a project!</h5>
      </b-row>
    </b-container>
  </b-modal>
</template>

<script>
export default {
  data() {
    return {
      project: {
        name: null,
        experiment_date: null,
        analyzed: null,
        observation: null,
        id: null
      },
      alert: null,
      showAlert: false
    };
  },

  methods: {
    closeEdit() {
      setTimeout(() => {
        this.hideModal();
        this.$store.dispatch("loadProjects");
        this.showAlert = false;
        this.$store.dispatch("clearUpdateMsg");
      }, 1500);
    },

    async modifyProject() {
      await this.$store.dispatch("updateProject", this.project).then(() => {
        this.showAlert = true;
        this.closeEdit();
      });
    },

    hideModal() {
      this.project = {
        name: null,
        experiment_date: null,
        analyzed: null,
        id: null,
        observations: null
      };
      this.$refs["edit-projects-modal"].hide();
    },

    async deleteCurrentProject() {
      await this.$store
        .dispatch("deleteCurrentProject", this.project)
        .then(() => {
          this.showAlert = true;
        });

      setTimeout(() => {
        this.hideModal();
        this.$store.dispatch("clearProjects");
        this.$store.dispatch("loadProjects");
        this.$store.dispatch("clearCurrentProject");

        this.showAlert = false;
        this.$store.dispatch("clearUpdateMsg");
      }, 1500);
    }
  },

  computed: {
    currentProject() {
      return this.$store.getters.currentProject;
    },
    updateMsg() {
      return this.$store.getters.updateMsg;
    }
  }
};
</script>

<style>
</style>