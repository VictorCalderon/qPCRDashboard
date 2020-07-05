<template>
  <div style="height: 405px; width: 100%">
    <l-map
      v-if="showMap"
      :zoom="zoom"
      :center="center"
      :options="mapOptions"
      style="height: 100%"
      @update:center="centerUpdate"
      @update:zoom="zoomUpdate"
    >
      <l-tile-layer :url="url" :attribution="attribution" />
      <div v-for="(s, i) in samplingSites" :key="i">
        <l-circle
          :lat-lng="s.loc"
          :radius="s.totalSamples"
          :color="siteColor[i]"
          :fillColor="siteColor[i]"
          :opacity="0.8"
        >
          <l-tooltip :options="{ permanent: false, interactive: true }">
            <div @click="innerClick(s.description)">{{s.name}}</div>
          </l-tooltip>
        </l-circle>
      </div>
    </l-map>
  </div>
</template>

<script>
import { latLng } from "leaflet";
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
      zoom: 8,
      center: latLng(19.007237, -70.41502),
      url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      attribution:
        '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      currentZoom: 11.5,
      currentCenter: latLng(19.007237, -70.41502),
      showParagraph: false,
      mapOptions: {
        zoomSnap: 0.5
      },
      showMap: true,
      siteColor: ["#DD614A", "#F48668", "#5AB1BB", "#A5C882", "#F7DD72"]
    };
  },
  computed: {
    samplingSites() {
      return [
        {
          loc: latLng(18.4358, -69.9853),
          name: "Sede Central",
          totalSamples: 19800
        },
        {
          loc: latLng(19.4548, -70.6929),
          name: "Santiago",
          totalSamples: 12800
        },
        {
          loc: latLng(19.22064, -70.5632),
          name: "La Vega",
          totalSamples: 11000
        }
      ];
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
  }
};
</script>