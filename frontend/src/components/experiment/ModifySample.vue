<template>
  <div class="settings-cog">
    <b-dropdown right size="sm" variant="outline-secondary">
      <template v-slot:button-content>
        <i class="fas fa-tags"></i>
      </template>
      <b-container class="text-center">
        Change Label
        <hr />
        <div class="mx-2">
          <b-row v-for="(label, i) in customLabels" :key="i">
            <b-button
              :class="{current: label==result}"
              class="mb-1 py-2"
              variant="secondary"
              block
              size="sm"
              @click="updateSample(label)"
            >{{label}}</b-button>
          </b-row>
        </div>
      </b-container>
    </b-dropdown>
  </div>
</template>

<script>
export default {
  data() {
    return {
      customLabel: "Etiqueta",
      result: null
    };
  },
  methods: {
    updateSample(result) {
      this.result = result;
      this.$store.dispatch("updateSample", result);
    }
  },
  computed: {
    currentSample() {
      if (this.$store.getters.currentSample == null) return {};
      return this.$store.getters.currentSample;
    },
    customLabels() {
      if (this.$store.getters.customLabels) {
        return this.$store.getters.customLabels;
      }
      return ["DETECTED", "NOT DETECTED", "UNDETERMINED", "RETAINED"];
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
 