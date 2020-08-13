<template>
  <b-card
    class="sample-table"
    bg-variant="light"
    header-bg-variant="light"
    header-text-variant="black"
  >
    <template v-slot:header>
      <b-form-row>
        <b-col lg="5" md="6">
          <h5 class="my-2 thin-font text-center">Results Table</h5>
        </b-col>
        <b-col class="my-0 py-0">
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
        </b-col>
        <b-col class="my-0 py-0">
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
        </b-col>
        <b-col class="my-0 py-0">
          <b-button
            class="text-dark border"
            variant="light"
            id="filter-popover"
            size="md"
            v-b-tooltip.hover.top
            title="Filter samples"
          >
            <i class="fas fa-filter"></i>
          </b-button>
          <b-popover target="filter-popover" placement="bottom">
            <b-form-input
              v-model="filter"
              placeholder="Enter sample name"
              class="placeholder-light text-center bg-light borderless border-bottom my-1"
            ></b-form-input>
          </b-popover>
        </b-col>
        <b-col class="my-0 py-0">
          <b-button
            class="text-dark border"
            variant="light"
            @click="modifySample"
            id="modify-sample"
            size="md"
            v-b-tooltip.hover.top
            title="Edit selected sample"
            :disabled="!sampleSelected"
          >
            <i class="fas fa-pencil-alt"></i>
          </b-button>
        </b-col>
        <b-col class="my-0 py-0">
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
        </b-col>
      </b-form-row>
    </template>

    <b-form-row>
      <b-col>
        <b-table
          borderless
          selectable
          scrollable
          responsive
          hover
          sticky-header="73vh"
          head-variant="light"
          :fields="fields"
          :items="filteredTable"
          select-mode="single"
          :per-page="perPage"
          :current-page="currentPage"
          @row-selected="onRowSelected"
          class="text-center"
        >
          <template v-slot:head(sample)="data">
            <span>{{ data.label + ' Name'}}</span>
          </template>
          <template v-slot:cell(score)="data">
            <b
              :style="{color: data.item.score < 0.75 ? data.item.score < 0.25 ? '#CC2936' : '#F2BB05' : '#124E78' }"
            >{{ data.item.score }}</b>
          </template>
        </b-table>
      </b-col>
    </b-form-row>
  </b-card>
</template>

<script>
import FileDownload from "js-file-download";

export default {
  data() {
    return {
      filter: null,
      perPage: 14,
      currentPage: 1,
      selectedRow: null,
      fields: [
        { key: "sample", sortable: true },
        { key: "marker", sortable: true },
        { key: "score", sortable: true },
        { key: "cq", sortable: true },
      ]
    };
  },

  methods: {
    downloadSampleTable() {

      // Make sure the table has content
      if (this.currentTable.length > 1) {
        // Generate csv
        let file = [...this.currentTable.map(sample => { return Object.values(sample).slice(1, -1).join(',')})];
        const header = [...Object.keys(this.currentTable[0]).slice(1, -1)];

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

    onRowSelected(items) {
      this.selectedRow = items[0];
      this.$store.dispatch('selectSample', this.selectedRow)
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

    searchFilter() {
      if (this.filter == "") return null;
      else return this.filter;
    },

    currentTable() {
      return this.$store.getters.currentTable;
    },

    lastPage() {
      if (this.currentTable) {
        return Math.ceil(this.currentTable.length / this.perPage);
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
      if (this.filteredTable == null) return {};

      const firstSample = this.filteredTable.slice(0, 1);
      this.$store.dispatch('selectSample', firstSample[0]);
    },

    searchFilter() {
      this.$store.dispatch("filterSamples", this.filter);
    }
  }
};
</script>

<style lang="scss" scoped>
.sample-table {
  height: 85vh;
}

@media (max-width: 480px) {
  .sample-table {
    height: 90vh;
  }
}
</style>