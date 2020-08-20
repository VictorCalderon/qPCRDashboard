<template>
  <b-modal
    id="search-experiments-modal"
    ref="search-experiments-modal"
    class="text-center"
    button-size="sm"
    size="lg"
    scrollable
    header-bg-variant="dark"
    header-text-variant="light"
    title="Search qPCR Database"
    hide-footer
    @shown="queryExperiments"
  >
    <b-tabs content-class="mt-3" fill>
      <b-tab title="Experiments" lazy>
        <b-form-row class="pb-2 mx-1">
          <b-col lg="4" sm="12" class="text-center mt-2">
            <div class="text-center">
              <label for="input-experimentname">Experiment</label>
              <b-form-input
                id="input-experimentname"
                v-model="name"
                class="text-center"
                type="text"
                placeholder="Project 1"
              ></b-form-input>
            </div>
          </b-col>
          <b-col lg="4" sm="12" class="text-center mt-2">
            <div class="text-center">
              <label for="input-datepicker">Date</label>
              <b-form-datepicker
                id="input-datepicker"
                v-model="date"
                type="date"
                placeholder="2020-05-25"
              ></b-form-datepicker>
            </div>
          </b-col>
          <b-col lg="4" sm="12" class="text-center mt-2 small-table">
            <div class="text-center">
              <label for="input-method">Observations</label>
              <b-form-input
                id="input-method"
                v-model="observations"
                class="text-center"
                locale="en"
                placeholder="3rd sampling round"
              ></b-form-input>
            </div>
          </b-col>
        </b-form-row>
        <b-form-row v-if="queriedExperiments.length > 0" class="border my-2 mx-1 rounded">
          <b-col cols="12">
            <b-table
              :items="queriedExperiments"
              :fields="experimentFields"
              :tbody-tr-class="rowClass"
              :busy="loadingResults"
              responsive
              scrollable
              hover
              borderless
              selectable
              select-mode="single"
              @row-selected="onExperimentSelected"
              :per-page="perPage"
              :current-page="currentPageExperiments"
            >
              <template v-slot:cell(analyzed)="data">
                <span
                  :style="{color: data.item.analyzed ? '#004E98' : '#F2BB05'}"
                >{{ data.item.analyzed ? 'Yes' : 'No' }}</span>
              </template>
            </b-table>
          </b-col>
        </b-form-row>
        <b-form-row v-else align-h="center" class="border my-2 mx-1 rounded">
          <b-col>
            <div align-h="center">
              <h5 class="my-5 text-center">Your search had no matches</h5>
            </div>
          </b-col>
        </b-form-row>

        <hr />

        <b-form-row align="center">
          <b-col md="12" lg="6">
            <b-pagination
              align="center"
              v-model="currentPageExperiments"
              :total-rows="experimentRows"
              :per-page="perPage"
              aria-controls="my-table"
              id="paginator-experiments"
              class="text-center"
            ></b-pagination>
          </b-col>
          <b-col md="12" lg="6">
            <b-button size="md" variant="info" @click="queryExperiments" class="mx-1">Search</b-button>
            <b-button
              size="md"
              variant="success"
              @click="selectExperiment"
              :disabled="activeOpenExperiment"
              class="mx-1"
            >Open</b-button>
            <b-button size="md" variant="warning" @click="hideModal()" class="mx-1">Cancel</b-button>
          </b-col>
        </b-form-row>
      </b-tab>
      <b-tab title="Samples" lazy>
        <b-container>
          <b-form-row class="pb-2" align-h="center">
            <b-col cols="12">
              <div class="text-center">
                <label for="input-samplename">Sample Name</label>
                <b-form-input
                  id="input-samplename"
                  v-model="sample"
                  class="text-center"
                  placeholder="Start your search"
                ></b-form-input>
              </div>
            </b-col>
          </b-form-row>

          <b-form-row v-if="queriedSamples.length > 0" class="border my-2 rounded text-center">
            <b-col>
              <b-table
                :items="queriedSamples"
                :fields="sampleFields"
                :busy="loadingResults"
                hover
                borderless
                small
                selectable
                responsive
                scrollable
                select-mode="single"
                @row-selected="onSampleSelected"
                :per-page="perPage"
                :current-page="currentPageSamples"
                head-variant="light"
                class="mt-1 text-center"
              >
                <template v-slot:head(sample)="data">
                  <span>{{ data.label }}</span>
                </template>
                <template v-slot:head(amp_cq)>
                  <span>{{ 'Cq' }}</span>
                </template>
                <template v-slot:head(name)>
                  <span>{{ 'Run' }}</span>
                </template>
              </b-table>
            </b-col>
          </b-form-row>

          <b-form-row
            v-if="searched && queriedSamples.length == 0"
            class="border my-2 mx-1 rounded"
          >
            <b-col>
              <div align-h="center">
                <h5 class="my-5 text-center">Your search had no matches</h5>
              </div>
            </b-col>
          </b-form-row>
        </b-container>
        <hr />
        <b-form-row align="center">
          <b-col lg="6" md="12">
            <b-pagination
              align="center"
              v-model="currentPageSamples"
              :total-rows="sampleRows"
              :per-page="perPage"
              aria-controls="my-table"
              id="paginator-samples"
              class="text-center"
            ></b-pagination>
          </b-col>
          <b-col lg="6" md="12">
            <b-button size="md" variant="info" @click="querySamples" class="mx-1">Search</b-button>
            <b-button
              size="md"
              variant="success"
              @click="selectSample"
              :disabled="activeOpenSample"
              class="mx-1"
            >Open</b-button>
            <b-button size="md" variant="warning" @click="hideModal()" class="mx-1">Cancel</b-button>
          </b-col>
        </b-form-row>
      </b-tab>
    </b-tabs>
  </b-modal>
</template>

<script>
export default {
  data() {
    return {
      selectedExperiment: null,
      selectedSample: null,
      activeOpenExperiment: true,
      activeOpenSample: true,
      searched: false,
      loadingResults: false,
      perPage: 10,
      currentPageSamples: 1,
      currentPageExperiments: 1,
      experimentFields: [
        {
          key: "name",
          sortable: true
        },
        {
          key: "date",
          sortable: true
        },
        {
          key: "observations",
          sortable: true
        },
        {
          key: "analyzed",
          sortable: true,
          label: "Done"
        }
      ],
      sampleFields: [
        {
          key: "sample"
        },
        {
          key: "name",
        },
        {
          key: "marker",
        },
        {
          key: "amp_cq",
        }
      ],
      date: null,
      name: null,
      analyzed: null,
      observations: null,
      sample: null
    };
  },

  methods: {
    async queryExperiments() {
      const params = {
        name: this.name,
        date: this.date,
        analyzed: this.analyzed,
        observations: this.observations
      };
      this.loadingResults = true;
      await this.$store
        .dispatch("queryExperiments", params)
        .then((this.loadingResults = false));
    },

    async querySamples() {
      const params = {
        sample: this.sample
      };
      this.loadingResults = true;
      await this.$store.dispatch("querySamples", params).then(() => {
        this.searched = true;
        this.loadingResults = false;
      });
    },

    hideModal() {
      this.$refs["search-experiments-modal"].hide();
      this.searched = false;
    },

    onExperimentSelected(items) {
      this.selectedExperiment = items;
      this.activeOpenExperiment = false;
    },

    onSampleSelected(items) {
      this.selectedSample = items;
      this.activeOpenSample = false;
    },

    async selectExperiment() {
      if (this.selectExperiment) {
        await this.$store.dispatch("selectExperiment", this.selectedExperiment[0]);
        await this.$store.dispatch("loadCurrentTable");
        await this.$store.dispatch("loadCurrentExperimentFluorescences");
        await this.$store.dispatch('loadCurrentExperimentPCA');
        await this.$store.dispatch('loadCurrentExperimentMaxGrad');
        
        this.selectedExperiment = null;
        this.hideModal();
      }
    },

    async selectSample() {
      if (this.selectedSample) {

        // Query experiment to database
        await this.$store.dispatch('getExperiment', { experimentID: this.selectedSample[0].experiment_id });

        // Load relevant experiment data
        await this.$store.dispatch("loadCurrentTable");
        await this.$store.dispatch("loadCurrentExperimentFluorescences");
        await this.$store.dispatch('loadCurrentExperimentPCA')

        // Select sample
        await this.$store.dispatch('selectSample', this.selectedSample)

        // Clear search and hide modal
        this.selectedSample = null;
        this.hideModal();
      }
    },

    rowClass(item, type) {
      if (!item || type !== "row") return;
      if (item.analyzed === false) return "";
    }
  },

  computed: {
    queriedExperiments() {
      return this.$store.getters.queriedExperiments;
    },

    queriedSamples() {
      return this.$store.getters.queriedSamples;
    },

    sampleRows() {
      return this.queriedSamples.length;
    },

    experimentRows() {
      return this.queriedExperiments.length;
    }
  },

  mounted() {
    this.queryExperiments();
  }
};
</script>

<style lang="scss" scoped >
.sample-table {
  height: 90vh;
}

@media (max-width: 480px) {
  .sample-table {
    height: 90vh;
  }
}
</style>