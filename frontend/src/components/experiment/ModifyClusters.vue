<template>
  <div class="settings-cog">
    <b-dropdown right size="sm" variant="outline-secondary">
      <template v-slot:button-content>
        <i class="fas fa-tags"></i>
      </template>
      <b-container class="text-center">
        Change Axes
        <hr />
        <div class="mx-2">
          <b-form-select v-model="new_x" :options="options"></b-form-select>
          <b-form-select v-model="new_y" :options="options" size="sm" class="mt-3"></b-form-select>
        </div>
      </b-container>
    </b-dropdown>
  </div>
</template>

<script>
export default {
  data() {
    return {
      new_x: null,
      new_y: null
    };
  },
  methods: {
    updateAxis() {
      this.$store.dispatch("changeScatterAxis", result);
    }
  },
  computed: {
    currentProject() {
      if (this.$store.getters.currentProject == null) return {};
      return this.$store.getters.currentProject;
    },

    customLabels() {
      if (this.$store.getters.customLabels) {
        return this.$store.getters.customLabels;
      }
      return ["DETECTED", "NOT DETECTED", "UNDETERMINED", "RETAINED"];
    },

    options() {
      return [
        ...Object.keys(this.$store.getters.currentProjectResults.data).map(
          p => {
            return {
              value: p,
              text: p
            };
          }
        )
      ];
    }
  },
  watch: {
    currentSample() {
      this.result = this.currentSample.result;
    }
  }
};
</script>

<style>
</style>
 