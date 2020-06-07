<template>
  <div class="rounded" v-if="allProjects">
    <!-- <Projects></Projects> -->
    <div v-if="currentProject">
      <b-row class="m-3" align-h="center">
        <b-col cols="2" class="bg-light rounded m-1">
          <Samples></Samples>
        </b-col>
        <b-col cols="8" class="bg-light rounded m-1">
          <Amplification></Amplification>
        </b-col>
        <b-col cols="5" class="bg-light rounded m-1">
          <Clustering></Clustering>
        </b-col>
        <b-col cols="5" class="bg-light rounded m-1">
          <ExperimentResults></ExperimentResults>
        </b-col>
      </b-row>
      <b-row class="m-5" align-h="center"></b-row>
    </div>
    <b-row v-else align-h="center">
      <b-card class="text-center mt-3 rounded">
        <div
          class="rounded py-2"
        >You don't have any opened projects. Use the search engine or recent projects bar.</div>
        <b-row align-h="center" class="mt-3">
          <b-button variant="info" v-b-modal.search-projects-modal>Search Project</b-button>
        </b-row>
      </b-card>
    </b-row>
  </div>
  <div v-else>
    <b-row align-h="center">
      <b-card class="text-center mt-5 rounded">
        <div
          class="rounded py-2"
        >You don't have any projects. Add a new project and start analyzing your data.</div>
        <b-row align-h="center" class="mt-3">
          <b-button variant="info" v-b-modal.add-projects-modal>Add Project</b-button>
        </b-row>
      </b-card>
    </b-row>
  </div>
</template>

<script>
import ExperimentResults from "@/components/experiment/ExperimentResults";
import Amplification from "@/components/experiment/AmplificationPlot";
import Clustering from "@/components/experiment/ClusterPlot";
import Samples from "@/components/experiment/Samples";
// import Projects from "@/components/experiment/Projects";

export default {
  components: {
    Amplification,
    Clustering,
    Samples,
    ExperimentResults
    // Projects
  },

  methods: {
    loadExperiments() {
      this.$store.dispatch("loadProjects");
    }
  },

  computed: {
    currentProject() {
      return this.$store.getters.currentProject;
    },
    allProjects() {
      return this.$store.getters.allProjects;
    }
  },

  created() {
    this.loadExperiments();
  },

  data() {
    return {
      loading: false
    };
  }
};
</script>