<template>
  <div>
    <b-modal
      id="search-projects-modal"
      ref="search-projects-modal"
      class="center"
      title="Search Projects"
      button-size="sm"
      size="lg"
      scrollable
    >
      <b-container>
        <b-row>
          <b-col>
            <div class="text-center">
              <label for="input-projectname">Type name</label>
              <b-form-input
                id="input-projectname"
                v-model="project_name"
                class="text-center"
                placeholder="Enter project name"
              ></b-form-input>
            </div>
          </b-col>
          <b-col>
            <div class="text-center">
              <label for="input-datepicker">Choose a date</label>
              <b-form-datepicker
                id="input-datepicker"
                v-model="experiment_date"
                class="mb-2"
                locale="en"
                :date-format-options="{ year: 'numeric', month: 'short', day: '2-digit' }"
              ></b-form-datepicker>
            </div>
          </b-col>
          <b-col>
            <div class="text-center">
              <!-- <label for="input-analyzed">Filter analyzed</label> -->
              <b-form-group label="Project status">
                <b-row class="mt-2">
                  <b-col>
                    <b-form-radio v-model="analyzed" name="some-radios" value="true">Analyzed</b-form-radio>
                  </b-col>
                  <b-col>
                    <b-form-radio v-model="analyzed" name="some-radios" value="false">Pending</b-form-radio>
                  </b-col>
                </b-row>
              </b-form-group>
            </div>
          </b-col>
        </b-row>

        <b-row v-if="queriedProjects">
          <hr />
          <b-col>
            <b-table
              :items="queriedProjects"
              :fields="fields"
              :tbody-tr-class="rowClass"
              :busy="loadingResults"
              hover
              borderless
              small
              selectable
              select-mode="single"
              @row-selected="onRowSelected"
            ></b-table>
          </b-col>
        </b-row>
      </b-container>
      <template v-slot:modal-footer="{ search, open, cancel }">
        <b-button size="md" variant="info" @click="queryProjects">Search</b-button>
        <b-button size="md" variant="success" @click="selectProject" :disabled="activeOpen">Open</b-button>
        <b-button size="md" variant="warning" @click="cancel()">Cancel</b-button>
      </template>
    </b-modal>
  </div>
</template>

<script>
export default {
  data() {
    return {
      loadingResults: false,
      selectedProject: null,
      activeOpen: true,
      fields: [
        {
          key: "name",
          sortable: true
        },
        {
          key: "experiment_date",
          sortable: true
        },
        {
          key: "analyzed",
          sortable: true
        },
        {
          key: "observations",
          sortable: true
        }
      ],
      experiment_date: null,
      project_name: null,
      analyzed: null,
      observations: null
    };
  },

  methods: {
    async queryProjects() {
      const params = {
        project_name: this.project_name,
        experiment_date: this.experiment_date,
        analyzed: this.analyzed,
        observations: this.observations
      };

      this.loadingResults = true;
      await this.$store.dispatch("queryProjects", params);
      this.loadingResults = false;
    },

    hideModal() {
      this.$refs["search-projects-modal"].hide();
      // this.$store.dispatch("clearQuery");
    },

    onRowSelected(items) {
      this.selectedProject = items;
      this.activeOpen = false;
    },

    async selectProject() {
      await this.$store.dispatch("selectProject", this.selectedProject[0]);
      await this.$store.dispatch("loadCurrentSamples");
      await this.$store.dispatch("loadProjectqPCRs");
      await this.$store.dispatch("loadCurrentProjectResults");
      this.selectedProject = null;
      this.hideModal();
    },

    rowClass(item, type) {
      if (!item || type !== "row") return;
      if (item.analyzed === false) return "table-warning";
    }
  },

  computed: {
    queriedProjects() {
      return this.$store.getters.queriedProjects;
    }
  }
};
</script>

<style>
</style>