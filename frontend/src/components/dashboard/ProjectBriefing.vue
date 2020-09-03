<template>
  <b-card
    bg-variant="light"
    align="center"
    header="Service Briefing"
    header-bg-variant="dark"
    header-text-variant="white"
    class
  >
    <b-form-row>
      <b-col lg="6" md="12">
        <b-card class="my-0">
          <h6 class="card-subtitle my-1 text-muted">Samples</h6>
          <span>
            <h4>
              {{ briefingData.samples }}
              <i class="fas fa-dna text-info"></i>
            </h4>
          </span>
        </b-card>
      </b-col>
      <b-col lg="6" md="12">
        <b-card class="my-0">
          <h6 class="card-subtitle my-1 text-muted">Experiments</h6>
          <span>
            <h4>
              {{ briefingData.experiments }}
              <i class="fas fa-flask"></i>
            </h4>
          </span>
        </b-card>
      </b-col>
      <b-col lg="6" md="12">
        <b-card class="my-0 mt-2">
          <h6 class="card-subtitle my-1 text-muted">Pending</h6>
          <span>
            <h4>
              {{ briefingData.pending }}
              <i class="fas fa-exclamation-circle text-warning"></i>
            </h4>
          </span>
        </b-card>
      </b-col>
      <b-col lg="6" md="12">
        <b-card class="my-0 mt-2">
          <h6 class="card-subtitle my-1 text-muted">Reported</h6>
          <span>
            <h4>
              {{ briefingData.reported }}  
              <i class="fas fa-file-medical-alt"></i>
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
        .catch((e) => {
          console.log(e);
        });
    },
  },

  computed: {
    briefingData() {
      return this.$store.getters.briefingData;
    },
  },

  data() {
    return {
      loadingBriefing: false,
      tabs: ["all", "today"],
    };
  },

  async mounted() {
    await this.getBriefing();
  },
};
</script>

<style>
</style>