<template>
  <b-container fluid>
    <b-form-row class="mt-1" v-if="allExperiments">
      <b-col lg="8" md="6" sm="10">
        <b-form-row>
          <b-col>
            <b-card
              bg-variant="light"
              align="center"
              header="Target Group Detection Rate"
              header-bg-variant="dark"
              header-text-variant="white"
              class="my-1"
            >
              <AmplifiedSamples></AmplifiedSamples>
            </b-card>
          </b-col>
        </b-form-row>
        <b-form-row>
          <b-col>
            <b-card
              bg-variant="light"
              align="center"
              header="Geolocalized Samples"
              header-bg-variant="dark"
              header-text-variant="white"
              class="my-1"
            >
              <SampleLocationMap></SampleLocationMap>
            </b-card>
          </b-col>
        </b-form-row>
      </b-col>
      <b-col lg="4" md="6" sm="10">
        <b-form-row>
          <b-col class="my-1">
            <ProjectBriefing></ProjectBriefing>
          </b-col>
        </b-form-row>
        <b-form-row>
          <b-col>
            <b-card
              bg-variant="light"
              align="center"
              header="Protocol Distribution"
              header-bg-variant="dark"
              header-text-variant="white"
              class="my-1"
            >
              <ExperimentObservations></ExperimentObservations>
            </b-card>
          </b-col>
        </b-form-row>
        <b-form-row>
          <b-col>
            <b-card
              bg-variant="light"
              align="center"
              header="Prevalent Zones"
              header-bg-variant="dark"
              header-text-variant="white"
              class="my-1"
            >
              <LocatedSamplesCount></LocatedSamplesCount>
            </b-card>
          </b-col>
        </b-form-row>
      </b-col>
    </b-form-row>
    <b-form-row class="justify-content-center mt-5" v-else>
      <b-col cols="8">
        <b-card class="text-center mt-3 rounded">
          <div
            class="rounded py-2"
          >You don't seem to have any experiments on the platform, add an experiment to start your project.</div>
          <b-row align-h="center" class="mt-3">
            <b-button variant="info" v-b-modal.add-experiments-modal>Add Experiment</b-button>
          </b-row>
        </b-card>
      </b-col>
    </b-form-row>
  </b-container>
</template>

<script>
// import TimeSeries from "@/components/dashboard/TimeSeries.vue";
import AmplifiedSamples from "@/components/dashboard/AmplifiedSamples.vue";
import ExperimentObservations from "@/components/dashboard/ExperimentObservations.vue";
import ProjectBriefing from "@/components/dashboard/ProjectBriefing.vue";
import LocatedSamplesCount from "@/components/dashboard/LocatedSamplesCount.vue";
import SampleLocationMap from "@/components/dashboard/SampleLocationMap.vue";

export default {
  components: {
    AmplifiedSamples,
    ExperimentObservations,
    ProjectBriefing,
    LocatedSamplesCount,
    SampleLocationMap
  },

  computed: {
    allExperiments() {
      return this.$store.getters.allExperiments;
    },

    currentRoute() {
      return this.$route.name;
    }
  },

  watch: {
    currentRoute() {
      if (this.currentRoute == "Dashboard") {
        this.$store.dispatch("updateTagDistribution");
        this.$store.dispatch("updateBriefingData");
        this.$store.dispatch("ampStatusTimeline");
        this.$store.dispatch("updateSamplingSites");
      }
    }
  }
};
</script>

<style>
</style>