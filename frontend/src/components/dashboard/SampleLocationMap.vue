<template>
  <b-form-row>
    <l-map
      :zoom="mapZoom"
      :center="mapCenter"
      :options="mapOptions"
      class="locationmap-height"
      @update:center="centerUpdate"
      @update:zoom="zoomUpdate"
    >
      <l-tile-layer :url="url" :attribution="attribution" />
      <div v-for="(s, i) in samplingSites" :key="i">
        <l-circle
          :lat-lng="s.loc"
          :radius="+markerSize * 100"
          :color="s.bgColor"
          :fillColor="s.bgColor"
          :opacity="s.perc"
        >
          <l-tooltip :options="{ permanent: false, interactive: true }">
            <div @click="innerClick(s.description)">
              <div>
                <span class="text-bold">{{ s.name }}</span>
                <br />
                <span>Detected: {{ s.count }}</span>
                <br />
                <span>Percentage: {{ Math.round(s.perc * 100) }}%</span>
              </div>
            </div>
          </l-tooltip>
        </l-circle>
      </div>
    </l-map>
  </b-form-row>
</template>

<script>
import { LMap, LTileLayer, LCircle, LTooltip } from "vue2-leaflet";

export default {
  components: {
    LMap,
    LTileLayer,
    LCircle,
    LTooltip
  },
  data() {
    return {
      zoom: 12,
      url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      attribution:
        '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      currentZoom: 12,
      mapOptions: {
        zoomSnap: 0.5
      }
    };
  },
  computed: {
    mapCenter() {
      return this.$store.getters.mapCenter;
    },

    samplingSites() {
      return this.$store.getters.samplingSites;
    },

    markerSize() {
      return this.$store.getters.markerSize;
    },

    markerOpacity() {
      return this.$store.getters.markerOpacity;
    },

    mapZoom() {
      return this.$store.getters.mapZoom;
    }
  },

  methods: {
    zoomUpdate(zoom) {
      this.currentZoom = zoom;
    },

    centerUpdate(center) {
      this.currentCenter = center;
    },

    innerClick(description) {
      alert(description);
    }
  },

  mounted() {
    this.$store.dispatch("updateSamplingSites");
  },

  watch: {
    mapCenter() {
      this.centerUpdate();
    },

    markerSize() {
      this.centerUpdate();
    }
  }
};
</script>

<style lang='scss' scoped>
.locationmap-height {
  height: 420px;
}

@media (max-width: 480px) {
  .locationmap-height {
    height: 420px;
  }
}
</style>