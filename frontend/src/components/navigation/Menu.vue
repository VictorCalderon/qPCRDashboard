<template>
  <div>
    <b-navbar toggleable="lg" type="dark" variant="dark">
      <!-- Brand -->
      <b-navbar-brand href="#">
        <span>qPCR Dashboard</span>
      </b-navbar-brand>

      <!-- Toggleable button -->
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

      <!-- Collapse content-->
      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-item to="/" :class="{'text-uppercase': currentRoute == 'Dashboard'}">Overview</b-nav-item>
          <b-nav-item to="/Experiment" :class="{'text-uppercase': currentRoute == 'Experiment'}">Experiment</b-nav-item>
          <b-nav-item to="/Analysis" :class="{'text-uppercase': currentRoute == 'Analysis'}">Analysis</b-nav-item>
        </b-navbar-nav>

        <b-navbar-nav class="ml-auto">
          <b-nav-item
            v-b-modal.add-experiments-modal
            v-if="this.$route.name == 'Analysis' && allExperiments"
          >
            <span>
              <i class="fas fa-plus"></i>&nbsp;Add
            </span>
          </b-nav-item>
          <b-nav-item
            v-b-modal.search-experiments-modal
            v-if="this.$route.name == 'Analysis' && allExperiments"
          >
            <i class="fas fa-search"></i>&nbsp;
            <span class>Search</span>
          </b-nav-item>
          <b-nav-item 
            to="/Adjustments" 
            :class="{'text-uppercase': currentRoute == 'Adjustments'}"
          ><i class="fas fa-cog mr-1"></i>Adjustments
          </b-nav-item>
          <b-nav-item @click="logOut">
            <i class="fas fa-sign-out-alt"></i>&nbsp;Sign Out
          </b-nav-item>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
  </div>
</template>


<script>

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
    },

    currentRoute() {
      return this.$route.name
    }
  },
  methods: {
    async selectExperiment(experiment) {
      await this.$store.dispatch("selectExperiment", experiment);
      await this.$store.dispatch("loadCurrentSamples");
      await this.$store.dispatch("loadCurrentExperimentResults");
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