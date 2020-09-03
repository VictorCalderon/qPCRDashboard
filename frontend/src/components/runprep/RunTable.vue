<template>
  <b-container fluid>
    <b-form-row class="">
      <b-col cols='12'>
          <b-form-row v-for="row in rows" :key="row" class="my-3">
              <b-col cols=1 v-for="column in columns" :key="column">
                  <b-button 
                    class="border rounded btn-light"
                    :class="{'btn-dark': newSamples.find(s => s.well == row + column)}"
                  >{{ row }}{{ column }}</b-button>
              </b-col>
          </b-form-row>
      </b-col>
    </b-form-row>
  </b-container>
</template>

<script>
export default {
  computed: {
    newSamples() {
      return this.$store.getters.newSamplePlate;
    },

    rows() {
        return ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    },

    columns() {
        return [...Array(12).keys()].map(i => i + 1)
    }
  },
};
</script>

<style>
</style>