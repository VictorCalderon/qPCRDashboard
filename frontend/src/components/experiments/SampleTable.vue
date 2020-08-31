<template>
  <b-card
    class="sample-table"
    bg-variant="light"
    header-bg-variant="light"
    header-text-variant="black"
  >
    <template v-slot:header>
      <b-form-row class="justify-content-center">
        <b-col lg="4" md="6">
          <h5 class="my-2 mx-0 thin-font text-center h6">{{ currentExperiment.name }}</h5>
        </b-col>
        <b-col lg="5" offset-lg="1" md offset-md="1" offset-sm="0" offset="2">
          <b-button-group size="md">
            <b-button
              class="text-dark border"
              variant="light"
              id="previous-samples"
              size="md"
              v-b-tooltip.hover.top
              title="Previous page"
              @click="prevPage"
              :disabled="currentPage == 1"
            >
              <i class="fas fa-arrow-left"></i>
            </b-button>
            <b-button
              class="text-dark border"
              variant="light"
              id="next-samples"
              size="md"
              v-b-tooltip.hover.top
              title="Next page"
              @click="nextPage"
              :disabled="currentPage == lastPage"
            >
              <i class="fas fa-arrow-right"></i>
            </b-button>
            <b-button
              class="text-dark border"
              variant="light"
              id="table-filter"
              size="md"
              v-b-tooltip.hover.bottom
              title="Filter table"
            >
              <i class="fas fa-filter"></i>
            </b-button>
            <b-popover target="table-filter" placement="bottom">
              <b-form-row>
                <b-col cols="12" class="text-center">Filter Samples</b-col>
                <b-col cols="12">
                  <b-form-input
                    v-model="xSampleFilter"
                    placeholder="Enter sample name"
                    class="placeholder-light text-center bg-light borderless border-bottom my-1"
                    lazy
                  ></b-form-input>
                </b-col>
              </b-form-row>
              <b-form-row class="mt-2">
                <b-col cols="12" class="text-center">Filter Markers</b-col>
                <b-col cols="12">
                  <b-form-group label-for="dropdown-form-password" @submit.stop.prevent>
                    <b-form-select
                      v-model="xMarkerFilter"
                      :options="options"
                      size="sm"
                      placeholder="Select Marker"
                    ></b-form-select>
                  </b-form-group>
                </b-col>
              </b-form-row>

              <hr class="my-1" />

              <b-form-row>
                <b-col class="12">
                  <b-button block @click="clearFilters()">Clear Filters</b-button>
                </b-col>
              </b-form-row>
            </b-popover>
            <b-button
              class="text-dark border"
              variant="light"
              v-b-modal.edit-experiments-modal
              id="modify-sample"
              size="md"
              v-b-tooltip.hover.top
              title="Edit experiment"
            >
              <i class="fas fa-pencil-alt"></i>
            </b-button>
            <b-button
              class="text-dark border"
              variant="light"
              @click="downloadSampleTable"
              id="download-dataset"
              size="md"
              v-b-tooltip.hover.top
              title="Download this table"
            >
              <i class="fas fa-download"></i>
            </b-button>
          </b-button-group>
        </b-col>
      </b-form-row>
    </template>

    <b-form-row class="px-0">
      <b-table
        borderless
        selectable
        scrollable
        responsive
        hover
        sticky-header="80vh"
        head-variant="light"
        :fields="fields"
        :items="filteredTable"
        select-mode="multi"
        :per-page="perPage"
        :current-page="currentPage"
        @row-selected="onRowSelected"
        class="text-center"
      >
        <template v-slot:cell(sample)="data">
          <b
            :style="{color: currentSample.find(s => s.result_id == data.item.result_id) ? '#296EB4' : '#36382E' }"
          >{{ data.item.sample }}</b>
        </template>

        <template v-slot:cell(marker)="data">
          <b :style="{color: markerColor[data.item.marker] }">{{ data.item.marker }}</b>
        </template>

        <template v-slot:cell(score)="data">
          <b
            :style="{color: data.item.score < 0.75 ? data.item.score < 0.25 ? '#CC2936' : '#F2BB05' : '#124E78' }"
          >{{ data.item.score }}</b>
        </template>

        <template v-slot:cell(amp_status)="data">
          <b
            :style="{color: data.item.cq != 0 ? '#124E78' : '#CC2936' }"
          >{{ data.item.cq != 0 ? 'Yes' : 'No' }}</b>
        </template>
      </b-table>
    </b-form-row>
  </b-card>
</template>

<script>
import FileDownload from "js-file-download";

export default {
  data() {
    return {
      perPage: 20,
      currentPage: 1,
      selectedRow: null,
      xSampleFilter: null,
      xMarkerFilter: null,
      options: [{ 'text': 'All', 'value': null }],
      fields: [
        { key: "sample", sortable: true, label: "Samples" },
        { key: "marker", sortable: true },
        // { key: "amp_status", sortable: true, label: 'Amp'},
        { key: "cq", sortable: true, label: 'Ct' },
        // { key: "score", sortable: true },
      ]
    };
  },

  methods: {
    downloadSampleTable() {
      // Make sure the table has content
      if (this.filteredTable) {

        // Generate csv
        let file = [...this.filteredTable.map(sample => { return Object.values(sample).slice(1, -1).join(',')})];
        const header = [...Object.keys(this.filteredTable[0]).slice(1, -1)];

        // Add header
        file.unshift(header.join(','));

        // Join lines with \n
        file = file.join('\r\n');

        // Generate data blob
        file = new Blob([file], { type: "text/plain" });

        // Download file
        FileDownload(file, this.currentExperiment.name + '.txt');
      }

      else {
        alert('The table is empty.')
      }

    },

    updateMarkerFilter() {
      // Filter unique markers
      const markers = [...new Set(this.currentTable.map((p) => { return p.marker}))];

      // Transform to options format
      const newOptions = markers.map(m => { return { 'text': m, 'value': m }})

      // Generate options dictionary
      this.options = [{'text': 'All', 'value': null }, ...newOptions]
    },

    clearFilters() {
      this.xSampleFilter = null;
      this.xMarkerFilter = null;
      this.$root.$emit("bv::hide::popover", "table-filter")
    },

    onRowSelected(items) {
      this.selectedRow = items;
      this.$store.dispatch('selectSample', items)
    },

    editSelectedSample() {
      alert("Not Implemented");
    },

    prevPage() {
      this.currentPage -= 1;
      this.$root.$emit("bv::hide::tooltip", "previous-samples");
    },

    nextPage() {
      this.currentPage += 1;
      this.$root.$emit("bv::hide::tooltip", "next-samples");
    },

    modifySample() {
      alert("Implement me!");
    }
  },

  computed: {
    filteredTable() {
      return this.$store.getters.filteredTable;
    },

    sampleFilter() {
      return this.xSampleFilter != "" ? this.xSampleFilter : null
    },

    markerFilter() {
      return this.xMarkerFilter != "" ? this.xMarkerFilter : null
    },

    markerColor() {
      return this.$store.getters.markerColor
    },

    currentTable() {
      return this.$store.getters.currentTable;
    },

    lastPage() {
      if (this.filteredTable) {
        return Math.ceil(this.filteredTable.length / this.perPage);
      } else return 99;
    },

    sampleSelected() {
      return this.selectedRow ? true : false;
    },

    currentSample() {
      return this.$store.getters.currentSample;
    },

    currentExperiment() {
      return this.$store.getters.currentExperiment;
    }
  },

  watch: {
    filteredTable() {
      if (this.filteredTable == []) return [];
      if (this.selectedRow) return void 0;
      // else {
      //   const firstSample = this.filteredTable.slice(0, 1);
      //   this.$store.dispatch('selectSample', firstSample);
      // }
    },

    currentTable() {
      this.updateMarkerFilter()
    },

    async sampleFilter() {
      await this.$store.dispatch("modifySampleFilter", this.sampleFilter);
      this.currentPage = 1;
    },

    async markerFilter() {
      await this.$store.dispatch('modifyMarkerFilter', this.markerFilter)
      this.currentPage = 1;
    },

    selectedRow() {
      if (!this.selectedRow) {
        this.selectedRow = null
      }
    }
  },

  mounted() {
    this.updateMarkerFilter()
  }
};
</script>

<style lang="scss" scoped>
.sample-table {
  height: 90vh;
}

@media (max-width: 480px) {
  .sample-table {
    height: 750px;
  }
}
</style>