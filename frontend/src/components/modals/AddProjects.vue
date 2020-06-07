<template>
  <div>
    <b-modal
      id="add-projects-modal"
      ref="add-projects-modal"
      size="md"
      hide-footer
      button-size="md"
      title="Add a new experiment"
    >
      <b-row>
        <b-col>
          <b-alert v-model="showAlert" variant="info" class="text-center">{{ importMsg }}</b-alert>
        </b-col>
      </b-row>
      <b-row>
        <b-col>
          <b-form-group
            id="fieldset-1"
            :description="invalidProjectName"
            label="Enter your experiment's name"
            label-for="input-1"
            class="text-center"
          >
            <b-form-input
              id="input-1"
              v-model="name"
              :state="state"
              trim
              placeholder="SARS-CoV-2 Run 1"
              class="text-center"
            ></b-form-input>
          </b-form-group>
        </b-col>
      </b-row>
      <b-row>
        <b-col>
          <b-form-group
            description="If unsure of what to upload read the manual."
            label="Upload experiment"
            label-for="select-1"
            class="text-center"
          >
            <b-form-file
              v-model="file"
              placeholder="Choose a file"
              drop-placeholder="Drop a file"
              id="file-1"
            ></b-form-file>
          </b-form-group>
        </b-col>
      </b-row>
      <hr />
      <b-row class="mx-1">
        <b-col cols="7">
          <b-form-group
            description="This is the export format of your equipment."
            label="Experiment Format"
            label-for="select-1"
            class="text-center"
          >
            <b-form-select id="select-1" v-model="format" :options="options" size="md"></b-form-select>
          </b-form-group>
        </b-col>
        <b-col cols="5">
          <b-form-group
            description="This will help us organize and analyze your data."
            label="Experiment date"
            label-for="experiment-date"
            class="text-center"
          >
            <b-form-datepicker
              id="experiment-date"
              v-model="date"
              class="mb-2"
              placeholder="YYYY-MM-DD"
              :date-format-options="{ year: 'numeric', month: 'numeric', day: 'numeric' }"
              locale="en"
            ></b-form-datepicker>
          </b-form-group>
        </b-col>
      </b-row>
      <hr />
      <b-container>
        <b-row>
          <b-col>
            <b-button @click="uploadExperiment" variant="outline-success" block>Upload Project</b-button>
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
export default {
  methods: {
    getToday() {
      // Get today
      let today = new Date();

      // Get day. month, year
      const dd = String(today.getDate()).padStart(2, "0");
      const mm = String(today.getMonth() + 1).padStart(2, "0");
      const yyyy = today.getFullYear();

      // Set variable
      this.date = yyyy + "-" + mm + "-" + dd;
    },

    async updateData() {
      await this.$store.dispatch("loadProjects");
      await this.$store.dispatch("loadLastProject");
      await this.$store.dispatch("selectCurrentProject");
    },

    hideModal() {
      this.$refs["add-projects-modal"].hide();
      this.name = "";
      this.file = null;
      this.showAlert = false;
    },

    async uploadExperiment() {
      // Empty form data
      let formData = new FormData();

      // Add user-input to form data
      formData.append("experiment_file", this.file);
      formData.append("experiment_name", this.name);
      formData.append("experiment_date", this.date);
      formData.append("experiment_format", this.format);

      // Dispatch uploadExperiment with formData
      await this.$store.dispatch("uploadExperiment", formData).then(() => {
        // Show alert
        this.showAlert = true;
      });

      // Update data
      await this.updateData();

      // Set timeout
      setTimeout(() => {
        this.hideModal();
        this.showAlert = false;
        this.$store.dispatch("clearImportMsg");
        this.$store.dispatch("loadLastProject");
      }, 1500);
    }
  },

  computed: {
    state() {
      if (this.name === "") {
        return null;
      }
      return this.name.length >= 5 ? true : false;
    },

    invalidProjectName() {
      if (this.name.length > 5) {
        return "This is how your experiment will be saved and queried.";
      } else if (this.name.length > 0) {
        return "Enter at least 5 characters";
      } else if (this.name == "") {
        return "Please enter the experiment name";
      } else {
        return "This is how your experiment will be saved and queried.";
      }
    },

    importMsg() {
      return this.$store.getters.importMsg;
    }
  },

  data() {
    return {
      showAlert: false,
      name: "",
      file: null,
      date: null,
      format: "QuantStudio",
      options: [
        { value: null, text: "Choose a format" },
        { value: "ABI7500", text: "Applied Biosystems (7500)" },
        { value: "QuantStudio", text: "Applied Biosystems (DS2)" },
        { value: "default", text: "qPCR Dashboard" }
      ]
    };
  },

  mounted() {
    this.getToday();
  }
};
</script>

<style>
</style>