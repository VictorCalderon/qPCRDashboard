<template>
  <div fixed="top">
    <b-navbar type="dark" variant="dark">
      <b-navbar-nav>
        <b-link class="navbar nav text-light" exact-active-class to="/">
          <span>Dashboard</span>
        </b-link>
        <b-link
          class="navbar nav text-light"
          exact-active-class
          to="/Experiments"
          v-if="allExperiments"
        >
          <span>Experiments</span>
        </b-link>
      </b-navbar-nav>

      <b-navbar-nav v-if="this.$route.name == 'Experiments' && allExperiments" class="ml-auto">
        <b-nav-item v-b-modal.add-experiments-modal class="mx-2">
          <i class="fas fa-plus"></i>&nbsp;Add
        </b-nav-item>
        <b-nav-item v-b-modal.search-experiments-modal class="mx-2">
          <i class="fas fa-search"></i>&nbsp;Search
        </b-nav-item>
        <b-nav-item v-b-modal.edit-experiments-modal class="mx-2" v-if="currentExperiment">
          <i class="far fa-edit"></i>&nbsp;Edit
        </b-nav-item>
        <b-nav-item @click="exportCurrentExperiment" class="mx-2" v-if="currentExperiment">
          <i class="fas fa-file-export" v-if="!exportingExperiment"></i>&nbsp;Export
        </b-nav-item>
        <b-nav-item class="mx-2" v-if="exportingExperiment">
          <b-spinner small type="grow" v-if="exportingExperiment"></b-spinner>Exporting...
        </b-nav-item>
        <b-nav-item disabled class="mx-2">
          <i class="fas fa-grip-lines-vertical"></i>
        </b-nav-item>
        <b-nav-item-dropdown right class="mx-2">
          <template v-slot:button-content>
            <span>
              <i class="fas fa-user"></i>&nbsp;User
            </span>
          </template>
          <b-dropdown-item href="#" @click="logOut">
            <i class="fas fa-sign-out-alt"></i>&nbsp;Sign Out
          </b-dropdown-item>
        </b-nav-item-dropdown>
      </b-navbar-nav>

      <b-navbar-nav v-if="this.$route.name == 'Dashboard'" class="ml-auto">
        <b-nav-item-dropdown right>
          <template v-slot:button-content>
            <span>
              <i class="fas fa-user"></i>&nbsp;User
            </span>
          </template>
          <b-dropdown-item href="#" @click="logOut">
            <i class="fas fa-sign-out-alt"></i>&nbsp;Sign Out
          </b-dropdown-item>
        </b-nav-item-dropdown>
      </b-navbar-nav>
    </b-navbar>
  </div>
</template>


<script>
import FileDownload from "js-file-download";
import axios from "axios";

export default {
  data() {
    return {
      showMessage: null,
      message: null,
      exportingExperiment: false
    };
  },
  computed: {
    allExperiments() {
      return this.$store.getters.allExperiments;
    },

    currentExperiment() {
      if (this.$store.getters.currentExperiment == null) {
        return null;
      }
      return this.$store.getters.currentExperiment;
    },

    currentUser() {
      return this.$store.getters.currentUser;
    }
  },
  methods: {
    async selectExperiment(experiment) {
      await this.$store.dispatch("selectExperiment", experiment);
      await this.$store.dispatch("loadCurrentSamples");
      await this.$store.dispatch("loadCurrentExperimentResults");
    },

    async exportCurrentExperiment() {
      this.exportingExperiment = true;
      let currentId = this.currentExperiment.id
      axios
        .get(`api/v1/experiments/export/${currentId}`)
        .then(res => {
          let file = res.data.file;

          if (file != null) {
            // Make a blob with it
            file = new Blob([file], {
              type: "text/plain"
            });

            // Download file
            FileDownload(file, `${this.currentExperiment.name}.csv`);
          }
        })
        .then(() => {
          this.exportingExperiment = false;
        });
    },

    toggleAddExperiments() {
      this.$store.dispatch("toggleAddExperiments");
    },

    toggleSearchExperiments() {
      this.$store.dispatch("toggleSearchExperiments");
    },

    toggleSettingsModal() {
      this.$store.dispatch("toggleSettingsModal");
    },

    logOut() {
      this.$store.dispatch("authLogOut");
    }
  }
};
</script>

<style lang="scss" scoped>
</style>