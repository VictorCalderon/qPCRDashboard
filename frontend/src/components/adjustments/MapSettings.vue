<template>
  <b-card
    bg-variant="light"
    align="center"
    header="Map Center and Markers Settings"
    header-bg-variant="dark"
    header-text-variant="white"
    class="m-2"
  >
    <div>
      <b-form-row class="justify-content-center">
        <b-col cols="6">
          <h5 class="font-weight-light">Latitude</h5>
          <b-form-input
            id="center-langitude"
            type="number"
            v-model="newMapCenter[0]"
            class="text-center"
          ></b-form-input>
        </b-col>
        <b-col cols="6">
          <h5 class="font-weight-light">Longitude</h5>
          <b-form-input
            id="center-longitude"
            type="number"
            v-model="newMapCenter[1]"
            class="text-center"
          ></b-form-input>
        </b-col>
      </b-form-row>
      <b-form-row class="justify-content-center mt-2">
        <b-col cols="3" v-if="!updatingMapCenter">
          <b-button
            block
            class="px-1"
            size="md"
            variant="info"
            id="save-map-center"
            @click="updateMapCenter"
            :disabled="noCenterChange"
            v-b-tooltip.hover
            title="Save changes"
          >
            <i class="fas fa-save"></i>
          </b-button>
        </b-col>
        <b-col cols="3" v-if="updatingMapCenter">
          <b-button class="px-1" size="md" id="update-map-center" variant="success" @click="updateMapCenter" block>
            <i class="fas fa-check-square"></i>
          </b-button>
        </b-col>
        <b-col cols="3">
          <b-button
            id="secret-text"
            block
            class="px-1"
            size="md"
            variant="warning"
            v-b-tooltip.hover
            title="Reset to default"
            @click="resetMarkerSize"
            :disabled="newMarkerSize==10000"
          >
            <i class="fas fa-redo-alt"></i>
          </b-button>
        </b-col>
      </b-form-row>
    </div>

    <hr class="my-4" />

    <div>
      <b-form-row class="justify-content-center">
        <b-col cols="6">
          <h5 class="font-weight-light">Marker size</h5>
          <b-form-input
            class="text-center"
            id="marker-size-offset"
            type="number"
            v-model="newMarkerSize"
          ></b-form-input>
        </b-col>
        <b-col cols="6">
          <h5 class="font-weight-light">Marker opacity</h5>
          <b-form-input
            class="text-center"
            id="marker-opacity-offset"
            type="number"
            v-model="newMarkerOpacity"
          ></b-form-input>
        </b-col>
      </b-form-row>
      <b-form-row class="justify-content-center mt-2">
        <b-col cols="3" v-if="!updatingMarkerSize && !updatingMarkerOpacity">
          <b-button
            block
            class="px-1"
            size="md"
            variant="info"
            id="save-marker-size"
            v-b-tooltip.hover
            title="Save changes"
            @click="updateMarkerSizeOpacity"
            :disabled="newMarkerSize==markerSize && newMarkerOpacity==markerOpacity"
            v-if="!updatingMarkerSize || !updatingMarkerOpacity"
          >
            <i class="fas fa-save"></i>
          </b-button>
        </b-col>

        <b-col cols="3" v-if="updatingMarkerSize || updatingMarkerOpacity">
          <b-button
            block
            class="px-1"
            size="md"
            variant="success"
            id="save-marker-size"
            v-b-tooltip.hover
            title="Changes saved"
          >
            <i class="fas fa-check-square"></i>
          </b-button>
        </b-col>

        <b-col cols="3">
          <b-button
            id="secret-text"
            block
            class="px-1"
            size="md"
            variant="warning"
            v-b-tooltip.hover
            title="Reset to default"
            @click="resetMarkerSizeOpacity"
            :disabled="newMarkerSize==50 && newMarkerOpacity==0.8"
          >
            <i class="fas fa-redo-alt"></i>
          </b-button>
        </b-col>
      </b-form-row>
    </div>
  </b-card>
</template>

<script>
export default {
  data() {
    return {
      updatingMapCenter: false,
      updatingMarkerSize: false,
      updatingMarkerOpacity: false,
      newMapCenter: [],
      newMarkerSize: null,
      newMarkerOpacity: null
    };
  },

  computed: {
    noCenterChange() {
      if (this.mapCenter) {
        return (
          this.newMapCenter[0] == this.mapCenter[0] &&
          this.newMapCenter[1] == this.mapCenter[1]
        );
      }
      else return false

    },

    mapCenter() {
      return this.$store.getters.mapCenter;
    },

    markerSize() {
      return this.$store.getters.markerSize;
    },

    markerOpacity() {
      return this.$store.getters.markerOpacity;
    }
  },

  methods: {
    updateMapCenter() {
      // Run action
      this.$store.dispatch("updateMapCenter", this.newMapCenter);
      // Set update bool
      this.updatingMapCenter = !this.updatingMapCenter;
      // Reset update bool
      setTimeout(() => {
        this.updatingMapCenter = !this.updatingMapCenter;
      }, 2000);
    },

    updateMarkerSize() {
      this.$store.dispatch("updateMarkerSize", this.newMarkerSize);
      this.updatingMarkerSize = !this.updatingMarkerSize;
      setTimeout(() => {
        this.updatingMarkerSize = !this.updatingMarkerSize;
      }, 2000);
    },

    updateMarkerOpacity() {
      this.$store.dispatch("updateMarkerOpacity", this.newMarkerOpacity);
      this.updatingMarkerOpacity = !this.updatingMarkerOpacity;
      setTimeout(() => {
        this.updatingMarkerOpacity = !this.updatingMarkerOpacity;
      }, 2000);
    },

    updateMarkerSizeOpacity() {
      if (this.newMarkerOpacity != this.markerOpacity) {
        this.updateMarkerOpacity()
      }

      if (this.newMarkerSize != this.markerSize) {
        this.updateMarkerSize()
      }
    },

    resetMarkerSizeOpacity() {
      this.resetMarkerSize;
      this.resetMarkerOpacity
    },

    resetMarkerSize() {
      this.$store.dispatch("updateMarkerSize", 10000);
      this.newMarkerSize = 10000;
    },

    resetMarkerOpacity() {
      this.$store.dispatch("updateMarkerOpacity", 0.8);
      this.newMarkerOpacity = 0.8;
    }
  },

  mounted() {
    // Map center init
    this.newMapCenter = [...this.mapCenter];

    // Marker size init
    this.newMarkerSize = this.markerSize;

    // Marker opacity init
    this.newMarkerOpacity = this.markerOpacity;
  },

  watch: {
    mapCenter() {
      // Map center init
      this.newMapCenter = [...this.mapCenter];
    },

    markerSize() {
      // Marker size init
      this.newMarkerSize = this.markerSize;
    },

    markerOpacity() {
      this.newMarkerOpacity = this.markerOpacity;
    }
  }
};
</script>

<style>
</style>