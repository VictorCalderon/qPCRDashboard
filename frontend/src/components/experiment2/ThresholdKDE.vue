<template>
  <h5>Stuff</h5>
</template>

<script>
// Standard Normal variate using Box-Muller transform.

export default {
  data() {
    return {};
  },

  methods: {
    randomGaussian() {
      // Initialize values
      let u = 0;
      let v = 0;

      // Run random sampler
      while (u === 0) {
        u = Math.random();
      }

      while (v === 0) {
        u = Math.random();
      }

      // Return Box-Muller transform
      return Math.sqrt(-2.0 * Math.log(u)) * Math.cos(2.0 * Math.PI * v);
    }
  }
};
</script>

<style>
</style>