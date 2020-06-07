<template>
  <div class="overflow-auto mt-3 py-2 mb-2 bg-light rounded">
    <div v-if="allProjects">
      <!-- <b-row align-h="center" class="py-0">
        <p class="py-0 my-0">Recent Projects</p>
      </b-row>-->
      <b-row class align-h="center">
        <b-button
          variant="outline-secondary"
          v-for="project in recentProjects"
          :key="project.id"
          @click="selectProject(project)"
          class="m-1"
          :pressed="currentProject.id == project.id"
        >
          <span>{{project.name | shortName }}</span>
        </b-button>
      </b-row>
    </div>
    <!-- <div v-else class="my-3">
      <b-row align-h="center">
        <p class="upload-projects">Upload a project to start analyzing your data</p>
      </b-row>
      <b-row align-h="center">
        <b-button variant="info" v-b-modal.add-projects-modal>Upload Project</b-button>
      </b-row>
    </div>-->
  </div>
</template>

<script>
export default {
  data() {
    return {
      current: null,
      projectListOffset: 0
    };
  },
  methods: {
    async selectProject(project) {
      await this.$store.dispatch("selectProject", project);
      await this.$store.dispatch("loadCurrentSamples");
      await this.$store.dispatch("loadProjectqPCRs");
    }
  },
  computed: {
    allProjects() {
      return this.$store.getters.allProjects;
    },

    recentProjects() {
      return this.$store.getters.recentProjects;
    },

    currentProject() {
      if (this.$store.getters.currentProject == null) {
        return {};
      }
      return this.$store.getters.currentProject;
    }
  }
};
</script>
<style lang='scss' scoped>
$GreyDarker: #505050;
$Indicator: #34a0e9;

.projects-header {
  color: $GreyDarker;
  font-size: 1.3rem;
  font-weight: 300;
  padding: 5px;
  font-weight: 300;
  margin: 0 10px 0 0px;
  padding: 10px 10px 6px 30px;
}

.no-projects {
  text-align: center;
  font-size: 1.5rem;
  font-weight: 300;
  padding-top: 10px;
}

.upload-projects {
  text-align: center;
  font-size: 1.3;
  font-weight: 300;
  padding-top: 10px;
}

.project-nav {
  display: block;
  padding: 1px 1px;
  margin-right: 20px;

  .page-button {
    font-size: 1.5rem;
    padding: 5px 0px;
    border-radius: 5px;
    border: none;
    background: none;
    cursor: pointer;

    .fas {
      color: $GreyDarker;
    }
    &:hover {
      background: $GreyDarker;
      color: white;

      .fas {
        color: white;
      }
    }

    &:disabled {
      &:hover {
        background: none;
        color: black;
      }

      .fas {
        color: black;
      }
    }
  }

  .project-list {
    display: grid;
    grid-template-columns: repeat(6, 1fr);

    .current {
      background: $GreyDarker;
      color: white;
    }
  }
  .project-item {
    background: none;
    text-align: center;
    color: black;
    padding: 10px 25px;
    border-radius: 5px;
    font-size: 0.9rem;
    font-weight: 400;
    border: 1px solid $GreyDarker;
    font-size: 300;
    margin: 0px 5px 5px 0px;

    &:hover {
      background: $GreyDarker;
      color: white;
      cursor: pointer;
    }
  }
}
</style>