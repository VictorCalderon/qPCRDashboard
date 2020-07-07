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
        <b-col class="m-2">
          <ProjectBriefing></ProjectBriefing>
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
            <LocatedSamplesCount></LocatedSamplesCount>
          </b-card>
        </b-col>
      </b-form-row>
    </b-col>
  </b-form-row>
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
  }
};
</script>

<style>
</style>