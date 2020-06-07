<template>
  <div class="wrapper">
    <modal-ChangeSettings v-if="changeSettingsModal"></modal-ChangeSettings>
    <modal-Login v-if="!accessToken"></modal-Login>
    <div v-else>
      <modal-SearchProjects></modal-SearchProjects>
      <modal-AddProjects></modal-AddProjects>
      <modal-EditProject></modal-EditProject>
      <modal-ExportProject></modal-ExportProject>
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
import AddProject from "@/components/modals/AddProjects";
import SearchProjects from "@/components/modals/SearchProjects";
import EditProject from "@/components/modals/EditProject";
import ExportProject from "@/components/modals/ExportProject";

import ChangeSettings from "@/components/modals/ChangeSettings";
import Login from "@/components/modals/LoginModal";

export default {
  components: {
    Menu,
    "modal-AddProjects": AddProject,
    "modal-SearchProjects": SearchProjects,
    "modal-ChangeSettings": ChangeSettings,
    "modal-Login": Login,
    "modal-EditProject": EditProject,
    "modal-ExportProject": ExportProject
  },

  computed: {
    addProjectsModal() {
      return this.$store.getters.addProjectsModal;
    },

    searchProjectsModal() {
      return this.$store.getters.searchProjectsModal;
    },

    changeSettingsModal() {
      return this.$store.getters.changeSettingsToggle;
    },

    accessToken() {
      return this.$store.getters.accessToken;
    },

    currentProject() {
      return this.$store.getters.currentProject;
    }
  },

  methods: {
    startApp() {
      this.$store.dispatch("loadProjects");
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