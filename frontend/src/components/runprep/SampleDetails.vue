<template>
  <b-container fluid>
    <b-form-row class>
      <b-col cols="12"></b-col>
    </b-form-row>
  </b-container>
</template>

<script>
export default {
  computed: {
    newSamples() {
      return this.$store.getters.newSamplePlate;
    },
  },
};
</script>

<style>
</style>