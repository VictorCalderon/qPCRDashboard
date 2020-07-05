<template>
  <b-form-row class="m-3 mt-3">
    <b-col lg="8" md="6" sm="10">
      <b-form-row>
        <b-col>
          <b-card
            bg-variant="light"
            align="center"
            header="Amplification Percetange by Marker"
            header-bg-variant="dark"
            header-text-variant="white"
            class="m-2"
          >
            <!-- <b-card-text>Percentage of amplified samples from the last 5 days</b-card-text> -->
            <AmplifiedSamples></AmplifiedSamples>
          </b-card>
        </b-col>
      </b-form-row>
      <b-form-row>
        <b-col>
          <b-card
            bg-variant="light"
            align="center"
            header="Mapped Collected Samples"
            header-bg-variant="dark"
            header-text-variant="white"
            class="m-2"
          >
            <SampleLocationMap></SampleLocationMap>
          </b-card>
        </b-col>
      </b-form-row>
    </b-col>
    <b-col lg="4" md="6" sm="10">
      <b-form-row>
        <b-col>
          <b-card
            bg-variant="light"
            align="center"
            header="Pending Experiments"
            header-bg-variant="dark"
            header-text-variant="white"
            class="m-2"
          >
            <b-card-text>Briefing of project's experiments and results</b-card-text>
            <PendingExperiments></PendingExperiments>
          </b-card>
        </b-col>
      </b-form-row>
      <b-form-row>
        <b-col>
          <b-card
            bg-variant="light"
            align="center"
            header="Experiment Tag Distribution"
            header-bg-variant="dark"
            header-text-variant="white"
            class="m-2"
          >
            <b-card-text>Ordered experiment tags from each experiment</b-card-text>
            <ExperimentObservations></ExperimentObservations>
          </b-card>
        </b-col>
      </b-form-row>
      <b-form-row>
        <b-col>
          <b-card
            bg-variant="light"
            align="center"
            header="Processed Experiments by Region"
            header-bg-variant="dark"
            header-text-variant="white"
            class="m-2"
          >
            <b-card-text>Sample collection site distribution</b-card-text>
            <LocatedSamplesCount></LocatedSamplesCount>
            <!-- <SampleLocationMap></SampleLocationMap> -->
          </b-card>
        </b-col>
      </b-form-row>
    </b-col>
    <!-- <b-col lg="8" md="6" sm="10"></b-col>

    <b-col lg="6" md="6" sm="10"></b-col>-->
  </b-form-row>
</template>

<script>
// import TimeSeries from "@/components/dashboard/TimeSeries.vue";
import AmplifiedSamples from "@/components/dashboard/AmplifiedSamples.vue";
import ExperimentObservations from "@/components/dashboard/ExperimentObservations.vue";
import PendingExperiments from "@/components/dashboard/PendingExperiments.vue";
import LocatedSamplesCount from "@/components/dashboard/LocatedSamplesCount.vue";
import SampleLocationMap from "@/components/dashboard/SampleLocationMap.vue";

export default {
  components: {
    // TimeSeries,
    AmplifiedSamples,
    ExperimentObservations,
    PendingExperiments,
    LocatedSamplesCount,
    SampleLocationMap
  }
};
</script>

<style>
</style>