<template>
  <b-container fluid>
    <b-modal
      ref="open-plate-add-search"
      id="open-plate-add-search"
      title="Add or Search Experiments"
      size="md"
      class="text-center"
      hide-footer
    >
      <b-form-row class="text-center">
        <NewExperiment></NewExperiment>
      </b-form-row>
    </b-modal>
    <b-modal
      ref="change-status"
      id="change-status"
      title="Change Sample Status"
      size="md"
      class="text-center"
      hide-footer
    >
      <b-form-row class="text-center">
        <b-col cols="12">
          <label for="experiment-name" class="text-center">Name of the Run</label>
          <b-form-input id="experiment-name" v-model="currentPlateName" type="text"></b-form-input>
        </b-col>
        <b-col cols="12">
          <b-button id="experiment-name-btn" size="md" class="mt-2 btn-success">Save</b-button>
        </b-col>
      </b-form-row>
    </b-modal>
    <keep-alive>
      <b-form-row class="mt-1" v-if="currentExperiment">
        <b-col lg="4" md="6" sm="12">
          <b-form-row>
            <b-col>
              <b-card
                bg-variant="light"
                align="center"
                header="Manage your Samples"
                header-bg-variant="dark"
                header-text-variant="white"
                class="my-1"
              >
                <NewSample></NewSample>
              </b-card>
            </b-col>
          </b-form-row>
        </b-col>
        <b-col lg="8" md="6" sm="12">
          <b-form-row>
            <b-col>
              <b-card
                bg-variant="light"
                align="center"
                :header="currentExperiment.name"
                header-bg-variant="dark"
                header-text-variant="white"
                class="my-1"
              >
                <RunPlate></RunPlate>
              </b-card>
            </b-col>
          </b-form-row>
        </b-col>
      </b-form-row>
      <b-form-row v-if="currentExperiment">
        <b-col cols="12">
          <b-card
            bg-variant="light"
            align="center"
            header="Sample Table"
            header-bg-variant="dark"
            header-text-variant="white"
            class="mt-2"
          >
            <NewSampleTable></NewSampleTable>
          </b-card>
        </b-col>
      </b-form-row>
      <b-form-row class="justify-content-center mt-5" v-if="!currentExperiment">
        <b-col cols="8">
          <b-card class="text-center mt-3 rounded">
            <div
              class="rounded py-2"
            >You don't seem to be working on any plates right now. Use the engine to search for plates or add a new one.</div>
            <b-row align-h="center" class="mt-3">
              <b-button variant="info" v-b-modal.open-plate-add-search>Add or Search plates</b-button>
            </b-row>
          </b-card>
        </b-col>
      </b-form-row>
    </keep-alive>
  </b-container>
</template>

<script>
// import FileDownload from "js-file-download";
import RunPlate from "@/components/experiment/RunPlate.vue";
import NewSample from "@/components/experiment/NewSample.vue";
import NewSampleTable from "@/components/experiment/NewSampleTable.vue";
import NewExperiment from "@/components/experiment/NewExperiment.vue";

export default {
  components: {
    RunPlate,
    NewSample,
    NewSampleTable,
    NewExperiment,
  },

  computed: {
    loadedExperiments() {
      return this.$store.getters.loadedExperiments; 
    },

    currentRoute() {
      return this.$route.name;
    },

    currentExperiment() {
      return this.$store.getters.currentExperiment;
    },
  },

  watch: {},

  data() {
    return {
      currentPlateName: "Test Data",
    };
  },

  methods: {
    saveSamplePlates() {
      alert("Implement me");
    },

    // downloadSampleTable() {
    //   // Make sure the table has content
    //   if (this.currentExperimentPlate) {
    //     // Generate csv
    //     let file = [
    //       ...this.filteredTable.map((sample) => {
    //         return Object.values(sample).slice(1, -1).join(",");
    //       }),
    //     ];
    //     const header = [...Object.keys(this.filteredTable[0]).slice(1, -1)];

    //     // Add header
    //     file.unshift(header.join(","));

    //     // Join lines with \n
    //     file = file.join("\r\n");

    //     // Generate data blob
    //     file = new Blob([file], { type: "text/plain" });

    //     // Download file
    //     FileDownload(file, this.currentPlateName.name + ".txt");
    //   } else {
    //     alert("The table is empty.");
    //   }
    // },
  },
};
</script>

<style>
</style>