<template>
  <b-card class="m-2" bg-variant="light" header-bg-variant="light" header-text-variant="black">
    <template v-slot:header>
      <b-form-row>
        <b-col cols="8">
          <h5 class="my-2 thin-font">Sample Table</h5>
        </b-col>
        <b-col class="my-0 py-0">
          <b-button
            class="text-dark border"
            variant="light"
            id="modify-sample"
            size="md"
            v-b-tooltip.hover.bottom
            title="Filter samples"
          >
            <i class="fas fa-search"></i>
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
      <b-col>
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
          :style="'height: 100%'"
        >
          <template v-slot:cell(amp)="data">
            <b
              :style="{color: data.item.amp ? '#6C8EAD' : '#FF3C38' }"
            >{{ data.item.amp ? 'Yes' : 'No' }}</b>
          </template>
        </b-table>
      </b-col>
    </b-form-row>
    <template v-slot:footer>
      <b-form-row class="my-0">
        <b-col cols="7" class="text-center">
          <b-pagination
            v-model="currentPage"
            :total-rows="sampleList.length"
            :per-page="perPage"
            aria-controls="my-table"
          >
            <template v-slot:first-text>
              <span class="text-secondary">First</span>
            </template>
            <template v-slot:prev-text>
              <span class="text-secondary">&lt;</span>
            </template>
            <template v-slot:next-text>
              <span class="text-secondary">&gt;</span>
            </template>
            <template v-slot:last-text>
              <span class="text-secondary">Last</span>
            </template>
          </b-pagination>
        </b-col>
      </b-form-row>
    </template>
  </b-card>
</template>

<script>
export default {
  data() {
    return {
      perPage: 10,
      currentPage: 1,
      selectedRow: null,
      fields: [
        { key: "well", sortable: true },
        { key: "sample", sortable: true },
        { key: "marker", sortable: true },
        { key: "amp", sortable: true },
        { key: "cq", sortable: true }
      ],
      sampleList: [
        {
          id: 0,
          well: "A1",
          sample: "2001231232M1",
          marker: "ORF1ab",
          amp: true,
          cq: 28
        },
        {
          id: 1,
          well: "B1",
          sample: "2001231232M1",
          marker: "ORF1ab",
          amp: false,
          cq: 0
        },
        {
          id: 2,
          well: "C1",
          sample: "2001231232M1",
          marker: "ORF1ab",
          amp: true,
          cq: 30
        },
        {
          id: 3,
          well: "D1",
          sample: "2001231232M1",
          marker: "ORF1ab",
          amp: true,
          cq: 27
        },
        {
          id: 4,
          well: "E1",
          sample: "2001231232M1",
          marker: "ORF1ab",
          amp: true,
          cq: 29
        },
        {
          id: 5,
          well: "F1",
          sample: "2001231232M1",
          marker: "ORF1ab",
          amp: true,
          cq: 24
        },
        {
          id: 6,
          well: "G1",
          sample: "2001231232M1",
          marker: "ORF1ab",
          amp: false,
          cq: 0
        },
        {
          id: 7,
          well: "H1",
          sample: "2001231232M1",
          marker: "ORF1ab",
          amp: true,
          cq: 26
        },
        {
          id: 8,
          well: "A2",
          sample: "2001231232M1",
          marker: "ORF1ab",
          amp: true,
          cq: 22
        },
        {
          id: 9,
          well: "B2",
          sample: "2001231232M1",
          marker: "ORF1ab",
          amp: true,
          cq: 26
        },
        {
          id: 10,
          well: "C2",
          sample: "2001231232M1",
          marker: "ORF1ab",
          amp: true,
          cq: 30
        },
        {
          id: 11,
          well: "D2",
          sample: "2001231232M1",
          marker: "ORF1ab",
          amp: true,
          cq: 21
        }
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
    }
  }
};
</script>

<style>
</style>