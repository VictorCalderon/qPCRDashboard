<template>
  <div class="wrapper">
    <modal-ChangeSettings v-if="changeSettingsModal"></modal-ChangeSettings>
    <modal-Login v-if="!accessToken"></modal-Login>
    <div v-else>
      <modal-SearchExperiments></modal-SearchExperiments>
      <modal-AddExperiments></modal-AddExperiments>
      <modal-EditExperiment></modal-EditExperiment>
      <modal-ExportExperiment></modal-ExportExperiment>
      <Menu></Menu>
      <b-row class="mx-0">
        <b-col>
          <keep-alive>
            <router-view />
          </keep-alive>
        </b-col>
      </b-row>
    </div>
  </div>
</template>

<script>
import Menu from "@/components/navigation/Menu";
import AddExperiment from "@/components/modals/AddExperiments";
import SearchExperiments from "@/components/modals/SearchExperiments";
import EditExperiment from "@/components/modals/EditExperiment";
import ExportExperiment from "@/components/modals/ExportExperiment";

import ChangeSettings from "@/components/modals/ChangeSettings";
import Login from "@/components/modals/LoginModal";

export default {
  components: {
    Menu,
    "modal-AddExperiments": AddExperiment,
    "modal-SearchExperiments": SearchExperiments,
    "modal-ChangeSettings": ChangeSettings,
    "modal-Login": Login,
    "modal-EditExperiment": EditExperiment,
    "modal-ExportExperiment": ExportExperiment
  },

  computed: {
    addExperimentsModal() {
      return this.$store.getters.addExperimentsModal;
    },

    searchExperimentsModal() {
      return this.$store.getters.searchExperimentsModal;
    },

    changeSettingsModal() {
      return this.$store.getters.changeSettingsToggle;
    },

    accessToken() {
      return this.$store.getters.accessToken;
    },

    currentExperiment() {
      return this.$store.getters.currentExperiment;
    }
  },

  methods: {
    startApp() {
      this.$store.dispatch("loadExperiments");
    }
  },

  watch: {
    accessToken() {
      this.startApp();
    }
  }
};
</script>

<style lang="scss">
$GreyLight: #d8d8d8;
$GreyDark: #969696;
$GreenRef: #00843d;
$GreenRefDark: #005c2b;
$GreenRefLight: #01a34d;
$GreyDarker: #505050;
$GreyBackground: #e6e6e6;
$GreyBackgroundDark: #535353;
$Indicator: #539ee4;

body {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

*:focus {
  outline: none !important;
  box-shadow: none !important;
}
</style>