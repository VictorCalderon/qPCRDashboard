<template>
  <b-card
    bg-variant="light"
    align="center"
    header="Project Statistics"
    header-bg-variant="dark"
    header-text-variant="white"
    class
  >
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
  </b-card>
</template>

<script>
export default {
  methods: {
    async getBriefing() {
      this.loadingBriefing = true;
      await this.$store
        .dispatch("updateBriefingData")
        .then((this.loadingBriefing = false))
        .catch(e => {
          console.log(e);
        });
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
  },

  async mounted() {
    await this.getBriefing();
  }
};
</script>

<style>
</style>