<template>
  <b-container flex="md">
    <b-row class="justify-content-center mt-3">
      <b-col sm="12" md="10" lg="6" class="text-center">
        <LocationSchema></LocationSchema>
      </b-col>
      <b-col sm="12" md="10" lg="6" class="text-center">
        <UserSettings></UserSettings>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import LocationSchema from "@/components/adjustments/LocationSchema.vue";
import UserSettings from "@/components/adjustments/UserSettings.vue";

export default {
  components: {
    LocationSchema,
    UserSettings
  }
};
</script>

<style>
</style>