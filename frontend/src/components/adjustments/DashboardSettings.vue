<template>
  <b-card
    bg-variant="light"
    align="center"
    header="Dashboard Settings"
    header-bg-variant="dark"
    header-text-variant="white"
    class="m-2"
  >
    <b-form-row class="justify-content-center border p-3">
      <b-form-row>
        <h4>Sampling Map</h4>
      </b-form-row>
      <b-form-row class="justify-content-center">
        <b-col cols="4">
          <label for="center-langitude">Latitude</label>
          <b-form-input
            class="text-center"
            id="center-langitude"
            type="number"
            v-model="newMapCenter[0]"
          ></b-form-input>
        </b-col>
        <b-col cols="4">
          <label for="center-langitude">Longitude</label>
          <b-form-input
            class="text-center"
            id="center-longitude"
            type="number"
            v-model="newMapCenter[1]"
          ></b-form-input>
        </b-col>
        <b-col cols="2">
          <label for="secret-text" class="my-1 text-light">Secret</label>
          <b-button
            block
            class="px-1"
            size="md"
            variant="info"
            id="secret-text"
            @click="updateMapCenter"
            v-if="notChanging"
            :disabled="noCenterChange"
          >
            <i class="fas fa-save"></i>
          </b-button>
          <b-button
            class
            variant="success"
            id="secret-text"
            @click="updateMapCenter"
            v-if="!notChanging"
          >Updated!</b-button>
        </b-col>
      </b-form-row>
    </b-form-row>
  </b-card>
</template>

<script>
export default {
  data() {
    return {
      notChanging: true,
      newMapCenter: []
    };
  },

  computed: {
    noCenterChange() {
      return (
        this.newMapCenter[0] == this.mapCenter[0] &&
        this.newMapCenter[1] == this.mapCenter[1]
      );
    },

    mapCenter() {
      return this.$store.getters.mapCenter;
    }
  },

  methods: {
    updateMapCenter() {
      this.$store.dispatch("updateMapCenter", this.newMapCenter);
      this.notChanging = !this.notChanging;
      setTimeout(() => {
        this.notChanging = !this.notChanging;
      }, 2000);
    }
  },

  mounted() {
    this.newMapCenter = [...this.mapCenter];
  }
};
</script>

<style>
</style>