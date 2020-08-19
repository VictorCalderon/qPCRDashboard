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
          <b-nav-item to="/Dashboard">Overview</b-nav-item>
          <b-nav-item to="/Experiments">Experiments</b-nav-item>
          <b-nav-item to="/Adjustments">Adjustments</b-nav-item>
        </b-navbar-nav>

        <b-navbar-nav class="ml-auto">
          <b-nav-item-dropdown
            text="Options"
            right
            v-if="this.$route.name == 'Experiments' && allExperiments"
          >
            <b-dropdown-item v-b-modal.add-experiments-modal>
              <i class="fas fa-plus text-dark"></i>&nbsp;
              <span class="text-dark">Add</span>
            </b-dropdown-item>
            <b-dropdown-item v-b-modal.search-experiments-modal>
              <i class="fas fa-search text-dark"></i>&nbsp;
              <span class="text-dark">Search</span>
            </b-dropdown-item>
            <b-dropdown-item v-b-modal.edit-experiments-modal v-if="currentExperiment">
              <i class="far fa-edit text-dark"></i>&nbsp;
              <span class="text-dark">Edit</span>
            </b-dropdown-item>
          </b-nav-item-dropdown>
          <b-nav-item-dropdown right>
            <!-- Using 'button-content' slot -->
            <template v-slot:button-content>User</template>
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