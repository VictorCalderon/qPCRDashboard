<template>
  <b-container flex="md">
    <b-form-row class="justify-content-center mt-3">
      <b-col sm="12" md="10" lg="7" class="text-center">
        <LocationSchema></LocationSchema>
      </b-col>
      <b-col sm="12" md="10" lg="5" class="text-center">
        <MapSettings></MapSettings>
      </b-col>
    </b-form-row>
  </b-container>
</template>

<script>
import LocationSchema from "@/components/adjustments/LocationSchema.vue";
import MapSettings from "@/components/adjustments/MapSettings.vue";

export default {
  components: {
    LocationSchema,
    MapSettings
  }
};
</script>

<style>
</style>