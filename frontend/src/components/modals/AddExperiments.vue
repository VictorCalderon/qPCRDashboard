<template>
  <b-modal
    id="add-experiments-modal"
    ref="add-experiments-modal"
    size="md"
    hide-footer
    button-size="md"
    title="Add a new experiment"
  >
    <b-form-row>
      <b-col>
        <b-alert
          v-model="showMessage"
          variant="info"
          class="text-center"
          dismissible
          fade
          @dismissed="hideModal"
        >{{ message }}</b-alert>
        <b-alert
          v-model="showError"
          variant="danger"
          class="text-center"
          dismissible
          fade
        >{{ message }}</b-alert>
      </b-col>
    </b-form-row>
    <b-form-row>
      <b-col>
        <b-form-group
          id="fieldset-1"
          :description="invalidExperimentName"
          label="Enter your experiment's name"
          label-for="input-experimentname"
          class="text-center"
        >
          <b-form-input
            id="input-experimentname"
            v-model="name"
            :state="state"
            trim
            placeholder="SARS-CoV-2 Run 1"
            class="text-center"
          ></b-form-input>
          <b-tooltip
            target="input-experimentname"
            triggers="hover"
            placement="right"
            variant="info"
          >"The title should contain enough information to be distinguishable from other experiments"</b-tooltip>
        </b-form-group>
      </b-col>
    </b-form-row>
    <b-form-row>
      <b-col>
        <b-form-group
          id="fieldset-1"
          description="Experiment tags that serve as variables."
          label="Enter your experiment's tags"
          label-for="input-experimenttags"
          class="text-center"
        >
          <b-form-tags
            id="tags"
            v-model="tags"
            class="text-center"
            tag-pills
            tag-variant="info"
            size="md"
            separator=" ,;"
            :input-attrs="{ 'aria-describedby': 'tags-remove-on-delete-help' }"
            remove-on-delete
          ></b-form-tags>
          <b-tooltip
            target="input-experimenttags"
            triggers="hover"
            placement="right"
            variant="info"
          >{{ tagsDescription }}</b-tooltip>
        </b-form-group>
      </b-col>
    </b-form-row>
    <b-form-row>
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
    </b-form-row>
    <hr />
    <b-form-row class="mx-1">
      <b-col cols="6">
        <b-form-group
          description="This is the export format of your equipment."
          label="Experiment Format"
          label-for="select-1"
          class="text-center"
        >
          <b-form-select
            id="select-1"
            v-model="format"
            :options="options"
            size="md"
            class="text-center"
          ></b-form-select>
        </b-form-group>
      </b-col>
      <b-col cols="6">
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
    </b-form-row>
    <hr />
    <b-container>
      <b-form-row>
        <b-col v-if="!uploading">
          <b-button @click="sendExperiment" variant="outline-success" block>Upload Experiment</b-button>
        </b-col>
        <b-col v-if="uploading">
          <b-button variant="info" disabled block>
            <b-spinner small type="grow"></b-spinner>
          </b-button>
        </b-col>
        <b-col>
          <b-button variant="outline-secondary" @click="hideModal" block>Close</b-button>
        </b-col>
      </b-form-row>
    </b-container>
  </b-modal>
</template>

<script>
import axios from "axios";
export default {
  methods: {
    async updateData() {
      await this.$store.dispatch("loadExperiments");
    },

    hideModal() {
      this.$refs["add-experiments-modal"].hide();
      this.name = "";
      this.file = null;
      this.message = false;
      this.showMessage = false;
      this.method = "";
      this.showError = false;
      this.uploading = false;
    },

    async sendExperiment() {
      this.uploading = true;
      // Empty form data
      let formData = new FormData();

      // Add user-input to form data
      formData.append("file", this.file);
      formData.append("name", this.name);
      formData.append("date", this.date);
      formData.append("tags", this.tags);
      formData.append("format", this.format);

      // Dispatch uploadExperiment with formData
      await axios
        .post("api/v1/experiments/import", formData, {
          headers: {
            "Content-Type": "multipart/form-data"
          }
        })
        .then(res => {
          this.uploading = false;
          this.message = res.data.msg;
          this.showMessage = true;
          this.$store.dispatch("loadExperiments");
          // this.$store.dispatch("getMarkers");
        })
        .catch(err => {
          this.message = err.response.data.msg;
          this.showError = true;
          this.uploading = false;
        });
    }
  },

  computed: {
    state() {
      if (this.name === "") {
        return null;
      }
      return this.name.length >= 5 ? true : false;
    },

    invalidExperimentName() {
      if (this.name.length > 5) {
        return "This is how your experiment will be saved and queried.";
      } else if (this.name.length > 0) {
        return "Enter at least 5 characters";
      } else if (this.name == "") {
        return "Please enter the experiment name.";
      } else {
        return "This is how your experiment will be saved and queried.";
      }
    }
  },

  data() {
    return {
      name: "",
      file: null,
      date: null,
      format: "zip",
      methodology: null,
      tags: [],
      message: false,
      showMessage: false,
      showError: false,
      uploading: false,
      methodDescription: "e.g. Experimental conditions or a brief description",
      tagsDescription: "e.g. Independent experiments variables",
      options: [
        { value: null, text: "Choose a format" },
        { value: "txt", text: "ABI 7500" },
        { value: "zip", text: "Design and Analysis 2" }
      ]
    };
  },

  mounted() {
    // this.getToday();
  }
};
</script>

<style>
</style>