<template>
  <b-navbar toggleable="lg" type="dark" variant="dark">
    <b-navbar-brand href="#">
      <span>qPCR Dashboard</span>
    </b-navbar-brand>

    <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

    <b-collapse id="nav-collapse" is-nav>
      <b-navbar-nav>
        <b-link class="navbar nav text-light" exact-active-class to="/Dashboard">
          <span
            :class="this.$route.name == 'Dashboard' ? 'custom-active-link' : 'custom-inactive-link'"
          >Overview</span>
        </b-link>
        <b-link
          class="navbar nav text-light"
          exact-active-class
          to="/Experiments"
          v-if="allExperiments"
        >
          <span
            :class="this.$route.name == 'Experiments' ? 'custom-active-link' : 'custom-inactive-link'"
          >Experiments</span>
        </b-link>
        <b-link
          class="navbar nav text-light"
          exact-active-class
          to="/Adjustments"
          v-if="allExperiments"
        >
          <span
            :class="this.$route.name == 'Adjustments' ? 'custom-active-link' : 'custom-inactive-link'"
          >Adjustments</span>
        </b-link>
      </b-navbar-nav>

      <b-navbar-nav class="ml-auto">
        <b-nav-item-dropdown
          class="navbar nav text-light"
          text="Options"
          right
          v-if="this.$route.name == 'Experiments' && allExperiments"
        >
          <b-dropdown-item v-b-modal.add-experiments-modal class="mx-2">
            <i class="fas fa-plus text-dark"></i>&nbsp;
            <span class="text-dark">Add</span>
          </b-dropdown-item>
          <b-dropdown-item v-b-modal.search-experiments-modal class="mx-2">
            <i class="fas fa-search text-dark"></i>&nbsp;
            <span class="text-dark">Search</span>
          </b-dropdown-item>
          <b-dropdown-item v-b-modal.edit-experiments-modal class="mx-2" v-if="currentExperiment">
            <i class="far fa-edit text-dark"></i>&nbsp;
            <span class="text-dark">Edit</span>
          </b-dropdown-item>
        </b-nav-item-dropdown>

        <b-nav-item-dropdown right class="navbar nav text-light" text="User">
          <b-dropdown-item href="#">
            <i class="fas fa-user"></i>
            &nbsp;{{ currentUser }}
          </b-dropdown-item>
          <b-dropdown-item href="#" @click="logOut">
            <i class="fas fa-sign-out-alt"></i>&nbsp;Sign Out
          </b-dropdown-item>
        </b-nav-item-dropdown>
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
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
      let currentId = this.currentExperiment.id;
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
.custom-active-link {
  color: white;
}

.custom-inactive-link {
  color: rgb(158, 158, 158);
}
</style>