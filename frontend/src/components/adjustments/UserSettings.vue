<template>
  <b-card
    bg-variant="light"
    align="center"
    header="User Settings"
    header-bg-variant="dark"
    header-text-variant="white"
    class="m-2"
  >
    <b-form-row class="justify-content-end">
      <b-col cols="3">
        <h5 class="my-2">Dashboard Map Center</h5>
      </b-col>
      <b-col cols="3">
        <label for="center-langitude">Latitude</label>
        <b-form-input id="center-langitude" type="number"></b-form-input>
      </b-col>
      <b-col cols="3">
        <label for="center-langitude">Longitude</label>
        <b-form-input id="center-longitude" type="number"></b-form-input>
      </b-col>
    </b-form-row>
  </b-card>
</template>

<script>
export default {};
</script>

<style>
</style>