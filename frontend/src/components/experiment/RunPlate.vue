<template>
  <b-container fluid>
    <b-form-row class>
      <b-modal ref="edit-sample" id="edit-sample" :title="modalTitle" size="sm" class="text-center" hide-footer>
        <b-form-row v-if="selectedSample">
          <b-col cols=12 class="text-center">
            Priority Level:
            <b>{{ priorityOptions.find(p => p.value == selectedSample.priority)['text'] }}</b>
          </b-col>
          <b-col cols=6 class="mt-3">
            <b-button class="mx-2" variant='info' @click="changeStep(1)">Set as Extracted</b-button>
          </b-col>
          <b-col cols=6 class="mt-3">
            <b-button class="mx-2" variant='warning' @click="changeStep(99)">Reject Sample</b-button>
          </b-col>
        </b-form-row>
      </b-modal>
      <b-col cols="12">
        <b-form-row v-for="row in rows" :key="row" class="my-3">
          <b-col cols="1" v-for="column in columns" :key="column">
            <b-button
              class="border rounded"
              :class="checkStep(samplePlate.find(s => s.well == row + column))"
              @click="editSample(row + column)"
            >{{ row }}{{ column }}</b-button>
          </b-col>
        </b-form-row>
      </b-col>
    </b-form-row>
  </b-container>
</template>

<script>
export default {
  data() {
    return {
      currentWell: null,
    };
  },
  methods: {
    editSample(sampleWell) {
      this.currentWell = sampleWell;

      if (this.selectedSample) {
        this.$refs["edit-sample"].show();
      }
    },

    changeStep(step) {
      this.selectedSample.step = step;
      this.$refs['edit-sample'].hide();
    },

    checkStep(sample) {
      if (sample) {
        if (sample.step == 0) {
          return 'btn-dark'
        }

        if (sample.step == 1) {
          return 'btn-info'
        }
        return 'btn-warning'
      }
      else return 'btn-light'
    },
  },
  computed: {
    samplePlate() {
      return this.$store.getters.newSamplePlate;
    },

    rows() {
      return ["A", "B", "C", "D", "E", "F", "G", "H"];
    },

    columns() {
      return [...Array(12).keys()].map((i) => i + 1);
    },

    selectedSample() {
      return this.samplePlate.find((s) => s.well == this.currentWell);
    },

    stepOptions() {
      return this.$store.getters.stepOptions;
    },

    priorityOptions() {
      return this.$store.getters.priorityOptions
    },

    modalTitle() {
      if (this.selectedSample) {
        return this.selectedSample.well + " - " + this.selectedSample.cedula;
      } else return "Select a sample";
    },
  },
};
</script>

<style>
</style>