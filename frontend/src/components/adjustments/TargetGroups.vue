<template>
  <b-card
    bg-variant="light"
    align="center"
    header="Target Groups"
    header-bg-variant="dark"
    header-text-variant="white"
    class="m-2"
    v-if="targetGroups"
  >
    <b-tooltip target="add-group" triggers="hover" placement="left" variant="info">
      Group names can be alpha-numerical.
      Groups cluster your amplified genes into a single category.
      <br />e.g.: Marker ORF1ab will belong to SARS-CoV-2 surveillance group.
    </b-tooltip>

    <template v-slot:header>
      <b-form-row class="justify-content-center mb-0">
        <b-col cols="8" offset="2">
          <h6 class="mb-0 mt-2">Target Groups Configuration</h6>
        </b-col>
        <b-col cols="1" class="ml-auto" v-if="!visible">
          <b-button
            id="add-group"
            block
            variant="secondary"
            :disabled="disableAddGroup"
            @click="toggleAddGroup"
            size="sm"
            class="px-1"
          >
            <i class="fas fa-plus-square"></i>
          </b-button>
        </b-col>
        <b-col cols="1" class="ml-auto" v-if="visible">
          <b-button
            block
            variant="secondary"
            :disabled="disableAddGroup"
            @click="toggleAddGroup"
            size="sm"
            class="px-1"
          >
            <i class="fas fa-minus-square"></i>
          </b-button>
        </b-col>
      </b-form-row>
    </template>
    <b-collapse id="group-form" v-model="visible">
      <b-form-row class="justify-content-center">
        <b-col cols="2" class="my-1">
          <label for="group-key">ID</label>
          <b-form-input
            id="group-key"
            aria-label="Key"
            placeholder="001"
            v-model="newGroup.key"
            class="text-center"
            size="sm"
          ></b-form-input>
        </b-col>
        <b-col cols="3" class="my-1">
          <label for="group-name">Group Name</label>
          <b-form-input
            id="group-name"
            aria-label="GroupName"
            placeholder="SARS-CoV-2"
            v-model="newGroup.name"
            class="text-center"
            size="sm"
          ></b-form-input>
        </b-col>
        <b-col cols="6" class="my-1">
          <label for="group-desc">Description</label>
          <b-form-input
            id="group-desc"
            aria-label="Description"
            placeholder="Target organisms or functions"
            v-model="newGroup.description"
            class="text-center"
            size="sm"
          ></b-form-input>
        </b-col>
      </b-form-row>
      <b-form-row class="justify-content-center">
        <b-col cols="2">
          <label for="secret-text" class="text-light">Save</label>
          <b-button
            block
            class="px-1"
            size="md"
            variant="info"
            id="secret-text"
            @click="saveGroup"
            :disabled="!formReady"
          >
            <i class="fas fa-save"></i>
          </b-button>
        </b-col>
        <b-col cols="3">
          <label for="cancel-group" class="text-light">Cancel</label>
          <b-button
            block
            class="px-1"
            size="md"
            variant="warning"
            id="cancel-group"
            @click="toggleAddGroup"
          >
            <i class="fas fa-window-close"></i>
          </b-button>
        </b-col>
        <b-col cols="12">
          <hr />
        </b-col>
      </b-form-row>
    </b-collapse>

    <b-form-row v-if="groups.length > 0" class="justify-content-center">
      <b-col>
        <b-table
          borderless
          selectable
          hover
          :items="groups"
          :fields="fields"
          responsive="sm"
          select-mode="single"
          @row-selected="onRowSelected"
        >
          <template v-slot:head(id)>
            <span>Group ID</span>
          </template>
          <template v-slot:head(group_name)>
            <span>Group Name</span>
          </template>
        </b-table>
      </b-col>
    </b-form-row>
    <b-form-row v-if="noTargetGroups">
      <b-col cols="12">
        <p class="no-targets">Click the plus button and add a surveillance target</p>
      </b-col>
    </b-form-row>
    <template v-slot:footer v-if="groups.length > 0">
      <b-form-row class="justify-content-end">
        <b-col cols="2">
          <b-button
            id="modify-group"
            class="px-1"
            block
            variant="warning"
            @click="toggleModifyGroup"
            :disabled="!selectedGroup"
            size="md"
            v-if="!modification"
          >
            <i class="fas fa-edit"></i>
          </b-button>
        </b-col>
        <b-col cols="2">
          <b-button
            class="px-1"
            id="delete-group"
            block
            variant="danger"
            @click="deleteGroup"
            :disabled="!selectedGroup"
            size="md"
          >
            <i class="fas fa-trash"></i>
          </b-button>
        </b-col>
      </b-form-row>
    </template>
  </b-card>
</template>

<script>
export default {
  data() {
    return {
      visible: false,
      modification: false,
      selectedGroup: null,
      fields: ["key", "name", "description"],
      newGroup: {
        id: null,
        key: null,
        name: null,
        description: null,
      },
      groups: []
    };
  },
  methods: {
    toggleCollapse() {
      this.visible = !this.visible;
    },

    onRowSelected(items) {
      this.selectedGroup = items[0];
    },

    addGroup() {
      // Check if group is present
      const keys = this.groups.filter(s => s.key == this.newGroup.key);
      const names = this.groups.filter(g => g.name == this.newGroup.name)

      // Add if condition is met
      if (keys.length > 0 || names.length > 0) {
        alert("ID or Group Name already in use!");
      }

      // Add group and clear inputs
      else this.groups.push({ ...this.newGroup });

      // Clear group
      this.cleanGroupForm();
    },

    cleanGroupForm() {
      // Clear id
      this.newGroup.key = null;

      // Clear location
      this.newGroup.name = null;
    },

    toggleModifyGroup() {
      // Set current select item as the item
      this.newGroup = { ...this.selectedGroup };

      // Toggle the modification collapse
      this.visible = true;
      this.modification = true;
    },

    deleteGroup() {
      this.$store
        .dispatch("deleteTargetGroup", this.selectedGroup).then(() => {
          this.loadGroups();
        });
    },

    toggleAddGroup() {
      // Clean groups
      this.cleanGroupForm();

      // Toggle add groups
      this.modification = false;
      this.visible = !this.visible;
    },

    saveGroup() {
      const newGroup = { ...this.newGroup };
      this.$store
        .dispatch("updateTargetGroups", newGroup)
        .then(() => {
          this.toggleAddGroup();
        })
        .then(() => {
          this.loadGroups();
        });
    },

    async loadGroups() {
      await this.$store.dispatch("getTargetGroups").then(() => {
        this.groups = [...this.targetGroups];
      });
    }
  },

  computed: {  
    noTargetGroups() {
      return this.groups.length == 0 & !this.visible & !this.modification
    },

    targetGroups() {
      return this.$store.getters.targetGroups;
    },

    disableAddGroup() {
      if (this.newGroup) {
        return false;
      } else return true;
    },

    formReady() {
      if ( this.newGroup.key && this.newGroup.name ) {
        return true;
      } else return false;
    }
  },

  async mounted() {
    // Get groups
    this.loadGroups();
  },

  watch: {
    targetGroups() {
      this.groups = [...this.targetGroups];
    },

    selectedGroup() {
      this.newGroup = { ...this.selectedGroup };
    }
  }
};
</script>


<style lang='scss' scoped>
.no-targets {
  font-size: 1.3rem;
  font-weight: 300;
  margin-top: 15px;
}
</style>