<template>
  <b-form-row class="justify-content-center mt-1">
    <b-col sm="12" md="10" lg="6">
      <b-form-row>
        <b-col cols="12">
          <LocationSchema></LocationSchema>
        </b-col>
        <b-col cols="12"></b-col>
      </b-form-row>
    </b-col>
    <b-col sm="12" md="10" lg="4">
      <b-form-row>
        <b-col cols="12">
          <MapSettings></MapSettings>
        </b-col>
        <b-col cols="12">
          <TargetGroups></TargetGroups>
        </b-col>
        <b-col cols="12">
          <MarkerTarget></MarkerTarget>
        </b-col>
      </b-form-row>
    </b-col>
  </b-form-row>
</template>

<script>
import LocationSchema from "@/components/adjustments/LocationSchema.vue";
import MapSettings from "@/components/adjustments/MapSettings.vue";
import TargetGroups from "@/components/adjustments/TargetGroups.vue";
import MarkerTarget from "@/components/adjustments/MarkerTarget.vue";

export default {
  components: {
    LocationSchema,
    MapSettings,
    TargetGroups,
    MarkerTarget
  }
};
</script>

<style>
</style>