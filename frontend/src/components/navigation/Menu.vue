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
        <!-- <b-nav-item-dropdown right class="mx-2">
          <template v-slot:button-content>
            <span>
              <i class="fas fa-clock"></i>&nbsp;Recent
            </span>
          </template>
          <b-dropdown-item
            v-for="experiment in recentExperiments"
            :key="experiment.id"
            @click="selectExperiment(experiment)"
            class="m-1"
          >
            <span>{{experiment.name | shortName }}</span>
          </b-dropdown-item>
        </b-nav-item-dropdown>-->
        <b-nav-item v-b-modal.edit-experiments-modal class="mx-2">
          <i class="far fa-edit"></i>&nbsp;Edit
        </b-nav-item>
        <b-nav-item v-b-modal.export-experiments-modal class="mx-2">
          <i class="fas fa-file-export"></i>&nbsp;Export
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
export default {
  data() {
    return {};
  },
  computed: {
    allExperiments() {
      return this.$store.getters.allExperiments;
    },

    currentExperiment() {
      if (this.$store.getters.currentExperiment == null) {
        return {};
      }
      return this.$store.getters.currentExperiment;
    },

    currentUser() {
      return this.$store.getters.currentUser;
    },

    recentExperiments() {
      return this.$store.getters.recentExperiments;
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
      this.$store.dispatch("clearToken");
    }
  }
};
</script>

<style lang="scss" scoped>
</style>