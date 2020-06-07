<template>
  <div fixed="top">
    <b-navbar type="dark" variant="dark">
      <b-navbar-nav>
        <b-link class="navbar nav text-light" exact-active-class to="/">
          <span>Dashboard</span>
        </b-link>
        <b-link class="navbar nav text-light" exact-active-class to="/Experiments">
          <span>Experiments</span>
        </b-link>
      </b-navbar-nav>

      <b-navbar-nav v-if="this.$route.name == 'Experiments'" class="ml-auto">
        <b-nav-item v-b-modal.add-projects-modal class="mx-2">
          <i class="fas fa-plus"></i>&nbsp;Add
        </b-nav-item>
        <b-nav-item v-b-modal.search-projects-modal class="mx-2">
          <i class="fas fa-search"></i>&nbsp;Search
        </b-nav-item>
        <b-nav-item-dropdown right class="mx-2">
          <!-- Using 'button-content' slot -->
          <template v-slot:button-content>
            <span>
              <i class="fas fa-clock"></i>&nbsp;Recent
            </span>
          </template>
          <b-dropdown-item
            v-for="project in recentProjects"
            :key="project.id"
            @click="selectProject(project)"
            class="m-1"
          >
            <span>{{project.name | shortName }}</span>
          </b-dropdown-item>
        </b-nav-item-dropdown>
        <b-nav-item v-b-modal.edit-projects-modal class="mx-2">
          <i class="far fa-edit"></i>&nbsp;Edit
        </b-nav-item>
        <b-nav-item v-b-modal.export-projects-modal class="mx-2">
          <i class="fas fa-file-export"></i>&nbsp;Export
        </b-nav-item>
        <b-nav-item disabled class="mx-2">
          <i class="fas fa-grip-lines-vertical"></i>
        </b-nav-item>
        <b-nav-item-dropdown right class="mx-2">
          <!-- Using 'button-content' slot -->
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
          <!-- Using 'button-content' slot -->
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
    allProjects() {
      return this.$store.getters.allProjects;
    },

    currentProject() {
      if (this.$store.getters.currentProject == null) {
        return {};
      }
      return this.$store.getters.currentProject;
    },

    currentUser() {
      return this.$store.getters.currentUser;
    },

    recentProjects() {
      return this.$store.getters.recentProjects;
    }
  },
  methods: {
    async selectProject(project) {
      await this.$store.dispatch("selectProject", project);
      await this.$store.dispatch("loadCurrentSamples");
      await this.$store.dispatch("loadProjectqPCRs");
      await this.$store.dispatch("loadCurrentProjectResults");
    },

    toggleAddProjects() {
      this.$store.dispatch("toggleAddProjects");
    },

    toggleSearchProjects() {
      this.$store.dispatch("toggleSearchProjects");
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