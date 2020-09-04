<template>
  <b-container fluid>
    <b-form-row class="mt-1">
      <b-modal
        ref="open-table"
        id="open-table"
        title="Change Sample Status"
        size="md"
        class="text-center"
        hide-footer
      >
        <b-form-row class="text-center">
          <b-col cols=12>
            <label for="experiment-name" class="text-center">Name of the Run</label>
            <b-form-input id="experiment-name" v-model="currentPlateName" type="text"></b-form-input>
          </b-col>
          <b-col cols=12>
            <!-- <label for="experiment-name-btn" class="text-center"></label> -->
            <b-button id="experiment-name-btn" size=md class="mt-2 btn-success">Save</b-button>
          </b-col>
        </b-form-row>
      </b-modal>
      <b-col lg="4" md="6" sm="12">
        <b-form-row>
          <b-col>
            <b-card
              bg-variant="light"
              align="center"
              header="Add or Modify Samples"
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
              header="Current Experiment Plate"
              header-bg-variant="dark"
              header-text-variant="white"
              class="my-1"
            >
              <template v-slot:header>
                <b-form-row class="my-0 py-0">
                  <b-col cols="1"></b-col>
                  <b-col cols="3"></b-col>
                  <b-col cols="4">Current Experiment Plate</b-col>
                  <b-col cols="2"></b-col>
                  <b-col cols="2">
                    <!-- <b-button
                      class="text-dark border ml-2"
                      variant="light"
                      @click="saveSamplePlates"
                      id="download-dataset"
                      size="sm"
                      v-b-tooltip.hover.top
                      v-b-modal.open-table
                      title="New Experiment"
                    >
                      <i class="far fa-plus-square"></i>
                    </b-button> -->
                    <b-button
                      class="text-dark border ml-2"
                      variant="light"
                      @click="saveSamplePlates"
                      id="download-dataset"
                      size="sm"
                      v-b-tooltip.hover.top
                      title="Save run plate"
                    >
                      <i class="fas fa-save"></i>
                    </b-button>
                    <b-button
                      class="text-dark border ml-2"
                      variant="light"
                      @click="downloadSampleTable"
                      id="download-dataset"
                      size="sm"
                      v-b-tooltip.hover.top
                      title="Export current plate"
                    >
                      <i class="fas fa-download"></i>
                    </b-button>
                  </b-col>
                </b-form-row>
              </template>
              <RunPlate></RunPlate>
            </b-card>
          </b-col>
        </b-form-row>
      </b-col>
    </b-form-row>
    <b-form-row>
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
  </b-container>
</template>

<script>
import FileDownload from "js-file-download";
import RunPlate from "@/components/experiment/RunPlate.vue";
import NewSample from "@/components/experiment/NewSample.vue";
import NewSampleTable from "@/components/experiment/NewSampleTable.vue";

export default {
  components: {
    RunPlate,
    NewSample,
    NewSampleTable,
  },

  computed: {
    allExperiments() {
      return this.$store.getters.allExperiments;
    },

    currentRoute() {
      return this.$route.name;
    },

    currentExperimentPlate() {
      return this.$store.getters.newSamplePlate;
    },
  },

  mounted() {
    this.$store.dispatch("getSampleLocationSchemas");
  },

  watch: {},

  data() {
    return {
      currentPlateName: "Test Data",
    };
  },

  methods: {
    saveSamplePlates() {
      alert('Implement me')
    },

    downloadSampleTable() {
      // Make sure the table has content
      if (this.currentExperimentPlate) {
        // Generate csv
        let file = [
          ...this.filteredTable.map((sample) => {
            return Object.values(sample).slice(1, -1).join(",");
          }),
        ];
        const header = [...Object.keys(this.filteredTable[0]).slice(1, -1)];

        // Add header
        file.unshift(header.join(","));

        // Join lines with \n
        file = file.join("\r\n");

        // Generate data blob
        file = new Blob([file], { type: "text/plain" });

        // Download file
        FileDownload(file, this.currentPlateName.name + ".txt");

      } else {
        alert("The table is empty.");
      }
    },
  },
};
</script>

<style>
</style>