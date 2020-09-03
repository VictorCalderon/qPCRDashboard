<template>
  <b-container fluid>
    <b-form-row class="mt-1">
      <b-col lg="4" md="6" sm="12">
        <b-form-row>
          <b-col>
            <b-card
              bg-variant="light"
              align="center"
              header="Add or Modify Sample"
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
              <AllSamples></AllSamples>
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
import AllSamples from "@/components/runprep/RunTable.vue";
import NewSample from "@/components/runprep/NewSample.vue";
import NewSampleTable from "@/components/runprep/NewSampleTable.vue";

export default {
  components: {
    AllSamples,
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
  },

  mounted() {
    this.$store.dispatch("getSampleLocationSchemas");
  },

  watch: {},
};
</script>

<style>
</style>