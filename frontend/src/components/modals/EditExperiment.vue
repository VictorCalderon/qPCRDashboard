<template>
  <b-modal
    id="edit-experiments-modal"
    ref="edit-experiments-modal"
    class="text-center"
    title="Edit Experiment"
    size="md"
    centered
    hide-footer
    scrollable
  >
    <b-container v-if="currentExperiment">
      <b-alert v-model="showAlert" variant="info" class="text-center">{{ updateMsg }}</b-alert>
      <b-row class="mb-2">
        <b-col>
          <div class="text-center">
            <label for="edit-experimentname">Type name</label>
            <b-form-input
              id="edit-experimentname"
              v-model="experiment.name"
              class="text-center"
              :placeholder="currentExperiment.name"
            ></b-form-input>
          </div>
        </b-col>
        <b-col>
          <div class="text-center">
            <label for="edit-datepicker">Choose a date</label>
            <b-form-datepicker
              id="edit-datepicker"
              v-model="experiment.date"
              class="mb-2"
              locale="en"
              :date-format-options="{ year: 'numeric', month: 'short', day: '2-digit' }"
              :placeholder="currentExperiment.date"
            ></b-form-datepicker>
          </div>
        </b-col>
      </b-row>
      <hr />
      <b-row class="mb-2" align-h="center">
        <b-col>
          <div class="text-center">
            <label for="edit-experimentmethod">Methodology</label>
            <b-form-input
              id="edit-experimentmethod"
              v-model="experiment.methodology"
              class="text-center"
              :placeholder="currentExperiment.methodology"
            ></b-form-input>
          </div>
        </b-col>
      </b-row>
      <b-row>
        <b-col cols="10" offset="1">
          <hr />
          <div class="text-center">
            <b-form-group label="Experiment status">
              <b-row class="mt-2">
                <b-col>
                  <b-form-radio
                    v-model="experiment.analyzed"
                    name="analyzed-radios"
                    value="true"
                  >Analyzed</b-form-radio>
                </b-col>
                <b-col>
                  <b-form-radio
                    v-model="experiment.analyzed"
                    name="analyzed-radios"
                    value="false"
                  >Pending</b-form-radio>
                </b-col>
              </b-row>
              <hr />
              <b-row class="mt-1">
                <b-col>
                  <label for="delete-experiment-button">Delete current experiment</label>
                  <b-button
                    id="delete-experiment-button"
                    size="md"
                    variant="outline-danger"
                    @click="deleteCurrentExperiment"
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
            id="update-experiment-button"
            size="md"
            variant="success"
            @click="modifyExperiment"
            block
          >Update</b-button>
        </b-col>
        <b-col>
          <b-button
            id="cancel-experiment-button"
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
        <h5 class="my-2">Please open a experiment!</h5>
      </b-row>
    </b-container>
  </b-modal>
</template>

<script>
export default {
  data() {
    return {
      experiment: {
        name: null,
        experiment_date: null,
        analyzed: null,
        methodology: null,
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
        this.$store.dispatch("loadExperiments");
        this.showAlert = false;
        this.$store.dispatch("clearUpdateMsg");
      }, 1500);
    },

    async modifyExperiment() {
      await this.$store
        .dispatch("updateExperiment", this.experiment)
        .then(() => {
          this.showAlert = true;
          this.closeEdit();
        });
    },

    hideModal() {
      this.experiment = {
        name: null,
        experiment_date: null,
        analyzed: null,
        id: null,
        methodology: null
      };
      this.$refs["edit-experiments-modal"].hide();
    },

    async deleteCurrentExperiment() {
      await this.$store
        .dispatch("deleteCurrentExperiment", this.experiment)
        .then(() => {
          this.showAlert = true;
        });

      setTimeout(() => {
        this.hideModal();
        this.$store.dispatch("clearExperiments");
        this.$store.dispatch("loadExperiments");
        this.$store.dispatch("clearCurrentExperiment");

        this.showAlert = false;
        this.$store.dispatch("clearUpdateMsg");
      }, 1500);
    }
  },

  computed: {
    currentExperiment() {
      return this.$store.getters.currentExperiment;
    },
    updateMsg() {
      return this.$store.getters.updateMsg;
    }
  }
};
</script>

<style>
</style>