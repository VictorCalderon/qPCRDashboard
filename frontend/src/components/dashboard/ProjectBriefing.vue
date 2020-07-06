<template>
  <b-card no-body bg-variant="light">
    <b-tabs card pills fill class="text-center">
      <b-tab v-for="(tab, i) in tabs" :key="i" lazy @click="getBriefing(tab)">
        <template v-slot:title>
          <b-spinner type="grow" small v-if="loadingBriefing"></b-spinner>
          &nbsp;{{ tab.toUpperCase() }}
        </template>
        <b-form-row>
          <b-col>
            <b-card>
              <h6 class="card-subtitle mb-2 text-muted">Samples</h6>
              <span>
                <h4>
                  {{ briefingData.samples }}
                  <i class="fas fa-virus"></i>
                </h4>
              </span>
            </b-card>
          </b-col>
          <b-col>
            <b-card>
              <h6 class="card-subtitle mb-2 text-muted">Experiments</h6>
              <span>
                <h4>
                  {{ briefingData.experiments }}
                  <i class="fas fa-flask"></i>
                </h4>
              </span>
            </b-card>
          </b-col>
        </b-form-row>
      </b-tab>
    </b-tabs>
  </b-card>
</template>

<script>
export default {
  methods: {
    async getBriefing(mode) {
      this.loadingBriefing = true;
      await this.$store
        .dispatch("updateBriefingData", mode)
        .then((this.loadingBriefing = false))
        .catch(alert("Your data could not be retreived at this moment."));
    }
  },
  computed: {
    briefingData() {
      return this.$store.getters.briefingData;
    }
  },
  data() {
    return {
      loadingBriefing: false,
      tabs: ["all", "today"]
    };
  }
};
</script>

<style>
</style>