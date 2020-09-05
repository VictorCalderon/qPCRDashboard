<template>
  <b-container fluid>
    <b-form-row>
      <b-col cols="12">
        <b-card no-body>
          <b-tabs card fill>
            <b-tab title="Add Experiment">
              <b-form-row>
                <b-col cols="6">
                  <b-form-group id="cedula-input" description="Run Name">
                    <b-form-input
                      class="text-center text-muted"
                      placeholder="Enter Experiment Name"
                      v-model="newExperiment.name"
                    ></b-form-input>
                  </b-form-group>
                </b-col>

                <b-col cols="6">
                  <b-form-group id="barcode-input" description="Run Date">
                    <b-form-input
                      class="text-center text-muted"
                      placeholder="Scan"
                      v-model="newExperiment.date"
                      type="date"
                    ></b-form-input>
                  </b-form-group>
                </b-col>
              </b-form-row>
              <hr />
              <b-form-row>
                <b-col cols="6">
                  <b-button block variant="outline-success" @click="addNewExperiment">Add</b-button>
                </b-col>
                <b-col cols="6">
                  <b-button block variant="outline-danger">Cancel</b-button>
                </b-col>
              </b-form-row>
            </b-tab>
            <b-tab title="Look for Experiment">
              <b-form-row>
                <b-col cols="12">
                  <b-form-group id="cedula-input" description="Run Name">
                    <b-form-input
                      class="text-center text-muted"
                      placeholder="Enter Experiment Name"
                      v-model="newExperiment.name"
                    ></b-form-input>
                  </b-form-group>
                </b-col>
              </b-form-row>
              <b-form-row>
                <b-col cols=12 v-if="loadedExperiments">
                  <b-table
                    striped
                    hover
                    selectable
                    scrollable
                    responsive
                    select-mode="single"
                    @row-selected="onRowSelected"
                    :items="loadedExperiments"
                    :fields="fields"
                  ></b-table>
                </b-col>
              </b-form-row>
              <!-- <b-form-row>
                <b-col cols="12">
                  <b-form-group id="barcode-input" description="Run Date">
                    <b-form-input
                      class="text-center text-muted"
                      placeholder="Scan"
                      v-model="newExperiment.date"
                      type="date"
                    ></b-form-input>
                  </b-form-group>
                </b-col>
              </b-form-row>-->
              <hr />
              <b-form-row>
                <b-col cols="6" v-if="selectedRow.length != 0">
                  <b-button
                    block
                    variant="outline-success"
                    @click="selectExperiment(selectedRow)"
                  >Open</b-button>
                </b-col>
                <b-col cols="6" v-else>
                  <b-button
                    block
                    variant="outline-success"
                    @click="selectExperiment(selectedRow)"
                  >Search</b-button>
                </b-col>
                <b-col cols="6">
                  <b-button block variant="outline-danger">Cancel</b-button>
                </b-col>
              </b-form-row>
            </b-tab>
          </b-tabs>
        </b-card>
      </b-col>
    </b-form-row>
  </b-container>
</template>

<script>
import { mapGetters, mapActions } from "vuex";

export default {
  data() {
    return {
      newExperiment: {
        name: null,
        date: null,
      },
      selectedRow: [],
      fields: [
        { key: "name", label: "Name" },
        { key: "date", label: "Date" },
        { key: "amplified", label: "Amplified" },
      ],
    };
  },
  computed: {
    ...mapGetters(["newSamples", "loadedExperiments"]),
  },

  methods: {
    ...mapActions(["selectExperiment"]),

    addNewExperiment() {
      this.$store.dispatch("addNewExperiment", {
        name: this.newExperiment.name,
        date: this.newExperiment.date,
      });
    },

    onRowSelected(items) {
      this.selectedRow = items[0];
    },
  },

  mounted() {
    this.$store.dispatch("loadOldExperiments");
  },
};
</script>

<style>
</style>