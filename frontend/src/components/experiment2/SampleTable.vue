<template>
  <b-card class="m-2" bg-variant="light" header-bg-variant="light" header-text-variant="black">
    <template v-slot:header>
      <b-form-row>
        <b-col cols="5">
          <h5 class="my-2 thin-font">Sample Table</h5>
        </b-col>
        <b-col class="my-0 py-0">
          <b-button
            class="text-dark border"
            variant="light"
            id="previous-samples"
            size="md"
            v-b-tooltip.hover.bottom
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
            v-b-tooltip.hover.bottom
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
            id="filter-samples"
            size="md"
            v-b-tooltip.hover.bottom
            title="Filter samples"
          >
            <i class="fas fa-filter"></i>
          </b-button>
        </b-col>
        <b-col class="my-0 py-0">
          <b-button
            class="text-dark border"
            variant="light"
            @click="modifySample"
            id="modify-sample"
            size="md"
            v-b-tooltip.hover.bottom
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
            v-b-tooltip.hover.bottom
            title="Download this table"
          >
            <i class="fas fa-download"></i>
          </b-button>
        </b-col>
      </b-form-row>
    </template>

    <b-form-row class="justify-content-center">
      <b-col style="height: 600px">
        <b-table
          borderless
          selectable
          scrollable
          responsive
          hover
          :fields="fields"
          :items="sampleList"
          select-mode="single"
          :per-page="perPage"
          :current-page="currentPage"
          @row-selected="onRowSelected"
          class="text-center"
        >
          <template v-slot:cell(amp)="data">
            <b
              :style="{color: data.item.amp ? '#6C8EAD' : '#FF3C38' }"
            >{{ data.item.amp ? 'Yes' : 'No' }}</b>
          </template>
        </b-table>
      </b-col>
    </b-form-row>
  </b-card>
</template>

<script>
export default {
  data() {
    return {
      perPage: 12,
      currentPage: 1,
      selectedRow: null,
      fields: [
        { key: "well", sortable: true },
        { key: "sample", sortable: true },
        { key: "marker", sortable: true },
        { key: "amp", sortable: true },
        { key: "cq", sortable: true }
      ]
    };
  },
  methods: {
    onRowSelected(items) {
      this.selectedRow = items[0];
    },

    downloadSampleTable() {
      alert("Not Implemented");
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
    sampleList() {
      return this.$store.getters.sampleList;
    },

    lastPage() {
      if (this.sampleList) {
        return Math.ceil(this.sampleList.length / this.perPage);
      } else return 99;
    },

    sampleSelected() {
      return this.selectedRow ? true : false;
    }
  }
};
</script>

<style>
</style>