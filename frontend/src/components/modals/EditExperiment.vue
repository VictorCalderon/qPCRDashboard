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
      <b-alert
        v-model="showAlert"
        variant="info"
        class="text-center"
        fade
        dismissible
        @dismissed="hideModal()"
      >{{ updateMsg }}</b-alert>
      <b-form-row class="mb-2">
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
      </b-form-row>
      <b-form-row class="mb-2" align-h="center">
        <b-col>
          <div class="text-center">
            <label for="edit-experimentobservations">Observations</label>
            <b-form-textarea
              id="textarea"
              v-model="experiment.observations"
              placeholder="Enter description"
              rows="3"
              max-rows="6"
            ></b-form-textarea>
          </div>
        </b-col>
      </b-form-row>
      <b-form-row class="mb-2" align-h="center">
        <b-col>
          <div class="text-center mt-1">
            <label for="edit-experimenttags">Experiment tags</label>
            <b-form-tags
              id="tags"
              v-model="experiment.tags"
              class="text-center"
              tag-pills
              tag-variant="info"
              size="md"
              separator=" ,;"
              :input-attrs="{ 'aria-describedby': 'tags-remove-on-delete-help' }"
              remove-on-delete
            ></b-form-tags>
          </div>
        </b-col>
      </b-form-row>
      <hr />
      <b-form-row align-h="center" v-if="!deleteConfirmation">
        <b-col cols="6">
          <div class="text-center">
            <label for="delete-experiment-button">Delete experiment</label>
            <b-button
              id="delete-experiment-button"
              size="md"
              variant="outline-danger"
              @click="deleteConfirmation = true"
              block
            >Delete</b-button>
            <p class="text-secondary pt-1 my-1">This cannot be undone.</p>
          </div>
        </b-col>
        <b-col>
          <div class="text-center">
            <label for="edit-experimentstatus">Experiment Status</label>
            <b-form-checkbox
              id="edit-experimentstatus"
              v-model="experiment.analyzed"
              name="check-button"
              size="lg"
              switch
              class="mt-1"
            >
              <span class="text-secondary">
                <small>{{ experiment.analyzed ? 'Yes' : 'No' }}</small>
              </span>
            </b-form-checkbox>
            <p
              class="text-secondary pt-2 my-1"
            >{{ experiment.analyzed ? "Experiment analyzed" : "Analysis pending..."}}</p>
          </div>
        </b-col>
      </b-form-row>
      <hr class="my-1" v-if="!deleteConfirmation" />
      <b-form-row v-if="deleteConfirmation" align-h="center">
        <div class="text-center">
          <p class="text-center">Are you sure? This cannot be undone</p>
        </div>
        <b-col cols="6">
          <b-button
            id="delete-experiment-button-no"
            size="md"
            variant="outline-secondary"
            @click="deleteConfirmation = false"
            block
          >Cancel</b-button>
        </b-col>
        <b-col cols="6">
          <b-button
            id="delete-experiment-button-yes"
            size="md"
            variant="danger"
            @click="deleteCurrentExperiment"
            block
          >Delete</b-button>
        </b-col>
      </b-form-row>
      <b-form-row class="mt-2" v-if="!deleteConfirmation">
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
      </b-form-row>
    </b-container>
    <b-container v-else>
      <b-form-row align-h="center">
        <h5 class="my-2">Please open a experiment!</h5>
      </b-form-row>
    </b-container>
  </b-modal>
</template>

<script>
export default {
  data() {
    return {
      experiment: {
        name: null,
        date: null,
        analyzed: null,
        observations: null,
        tags: [],
        id: null
      },
      alert: null,
      showAlert: false,
      deleteConfirmation: false
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
      this.$store.dispatch("loadExperiments");
      this.$refs["edit-experiments-modal"].hide();
      this.deleteConfirmation = false;
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
  },

  watch: {
    currentExperiment() {

      // Copy current experiment to local object
      this.experiment = { ...this.currentExperiment };

      // Check if a project was set
      if (this.currentExperiment.tags) {
        this.experiment.tags = this.experiment.tags.split(';')
      }
    }
  }
}

</script>

<style lang='css' scoped>
.big-table {
  display: inline-block;
}

@media (max-width: 480px) {
  .big-table {
    display: none;
  }
}
</style>