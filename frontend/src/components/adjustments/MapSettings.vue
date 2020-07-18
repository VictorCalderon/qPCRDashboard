<template>
  <b-card
    bg-variant="light"
    align="center"
    header="Map Settings"
    header-bg-variant="dark"
    header-text-variant="white"
    class="m-2"
  >
    <div>
      <b-form-row class="justify-content-center">
        <b-col cols="12">
          <h5 class="font-weight-light">Center [Lat, Long]</h5>
        </b-col>
        <b-col cols="4">
          <b-form-input id="center-langitude" type="number" v-model="newMapCenter[0]"></b-form-input>
        </b-col>
        <b-col cols="4">
          <b-form-input id="center-longitude" type="number" v-model="newMapCenter[1]"></b-form-input>
        </b-col>
        <b-col cols="2">
          <b-button
            block
            class="px-1"
            size="md"
            variant="info"
            id="save-map-center"
            @click="updateMapCenter"
            v-if="!updatingMapCenter"
            :disabled="noCenterChange"
            v-b-tooltip.hover
            title="Save changes"
          >
            <i class="fas fa-save"></i>
          </b-button>
          <b-button class variant="success" @click="updateMapCenter" v-if="updatingMapCenter">
            <i class="fas fa-check-square"></i>
          </b-button>
        </b-col>
      </b-form-row>
    </div>

    <hr class="my-4" />

    <div>
      <b-form-row class="justify-content-center">
        <b-col md="12" lg="6">
          <b-form-row>
            <b-col>
              <h5 class="font-weight-light">Marker size scaler</h5>
            </b-col>
          </b-form-row>

          <b-form-row>
            <b-col cols="5">
              <b-form-input
                class="text-center"
                id="marker-size-offset"
                type="number"
                v-model="newMarkerSize"
              ></b-form-input>
            </b-col>

            <b-col cols="3" v-if="!updatingMarkerSize">
              <b-button
                block
                class="px-1"
                size="md"
                variant="info"
                id="save-marker-size"
                v-b-tooltip.hover
                title="Save changes"
                @click="updateMarkerSize"
                :disabled="newMarkerSize==markerSize"
                v-if="!updatingMarkerSize"
              >
                <i class="fas fa-save"></i>
              </b-button>
            </b-col>

            <b-col cols="3" v-if="updatingMarkerSize">
              <b-button class variant="success" v-if="updatingMarkerSize">
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
        </b-col>
        <b-col md="12" lg="6">
          <b-form-row>
            <b-col>
              <h5 class="font-weight-light">Marker opacity</h5>
            </b-col>
          </b-form-row>

          <b-form-row>
            <b-col cols="5">
              <b-form-input
                class="text-center"
                id="marker-opacity-offset"
                type="number"
                v-model="newMarkerOpacity"
              ></b-form-input>
            </b-col>

            <b-col cols="3" v-if="!updatingMarkerOpacity">
              <b-button
                block
                class="px-1"
                size="md"
                variant="info"
                id="save-marker-opacity"
                v-b-tooltip.hover
                title="Save changes"
                @click="updateMarkerOpacity"
                :disabled="newMarkerOpacity==markerOpacity"
                v-if="!updatingMarkerOpacity"
              >
                <i class="fas fa-save"></i>
              </b-button>
            </b-col>

            <b-col cols="3" v-if="updatingMarkerOpacity">
              <b-button class variant="success" v-if="updatingMarkerOpacity">
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
                @click="resetMarkerOpacity"
                :disabled="newMarkerOpacity==0.8"
              >
                <i class="fas fa-redo-alt"></i>
              </b-button>
            </b-col>
          </b-form-row>
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
      newMapCenter: null,
      newMarkerSize: null,
      newMarkerOpacity: null
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