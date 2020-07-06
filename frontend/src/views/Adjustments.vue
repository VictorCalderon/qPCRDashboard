<template>
  <b-container flex="md">
    <b-form-row class="justify-content-center mt-3">
      <b-col sm="12" md="10" lg="6" class="text-center">
        <LocationSchema></LocationSchema>
      </b-col>
      <b-col sm="12" md="10" lg="6" class="text-center">
        <DashboardSettings></DashboardSettings>
      </b-col>
    </b-form-row>
  </b-container>
</template>

<script>
import LocationSchema from "@/components/adjustments/LocationSchema.vue";
import DashboardSettings from "@/components/adjustments/DashboardSettings.vue";

export default {
  components: {
    LocationSchema,
    DashboardSettings
  }
};
</script>

<style>
</style>