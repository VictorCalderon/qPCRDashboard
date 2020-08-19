<template>
  <b-card
    bg-variant="light"
    align="center"
    header="Marker Target"
    header-bg-variant="dark"
    header-text-variant="white"
    class="m-2"
  >
    <!-- <b-tooltip target="add-group" triggers="hover" placement="left" variant="info">
      Group names can be alpha-numerical.
      Groups cluster your amplified genes into a single category.
      <br />e.g.: Marker ORF1ab will belong to SARS-CoV-2 surveillance group.
    </b-tooltip>-->

    <template v-slot:header>
      <b-form-row class="justify-content-center mb-0">
        <b-col cols="12" offset>
          <h6 class="mb-0 mt-2">Marker Target Configuration</h6>
        </b-col>
      </b-form-row>
    </template>

    <b-form-row v-if="availableMarkers.length > 0">
      <b-table
        :items="markerList"
        :fields="fields"
        :perPage="perPage"
        :currentPage="currentPage"
        borderless
        small
        class="mb-0"
      >
        <template v-slot:cell(target_id)="data">
          <b-form-group>
            <b-form-select v-model="data.item.target_id" :options="targetGroupOptions" size="sm"></b-form-select>
          </b-form-group>
        </template>
      </b-table>
    </b-form-row>

    <template v-slot:footer v-if="markerList.length > 0">
      <b-form-row class="justify-content-end">
        <b-col cols="8">
          <b-pagination
            v-model="currentPage"
            :total-rows="rows"
            :per-page="perPage"
            aria-controls="my-table"
            class="my-0"
          ></b-pagination>
        </b-col>
        <b-col cols="2" v-if="!updatingMarkerTargets">
          <b-button
            id="modify-marker"
            class="px-1"
            block
            variant="warning"
            size="md"
            @click="modifyMarkers()"
          >
            <i class="fas fa-edit"></i>
          </b-button>
        </b-col>
        <b-col cols="2" v-if="updatingMarkerTargets">
          <b-button class="px-1" variant="success" size="md" block>
            <i class="fas fa-check-square"></i>
          </b-button>
        </b-col>
        <b-col cols="2">
          <b-button class="px-1" id="delete-marker" block variant="danger" size="md">
            <i class="fas fa-trash"></i>
          </b-button>
        </b-col>
      </b-form-row>
    </template>
  </b-card>
</template>

<script>
export default {
  
  mounted() {
    // Get markers
    this.$store.dispatch('getAvailableMarkers');
  },

  data() {
    return {
      updatingMarkerTargets: false,
      markerList: [],
      currentPage: 1,
      perPage: 3,
      fields: [
        { key: "marker", sortable: false, label: "Marker" },
        { key: "target_id", sortable: true, label: "Target Group" },
      ]
    }
  },

  methods: {
    async getAvailableMarkers() {
      await this.$store.dispatch('getAvailableMarkers')
    },

    async modifyMarkers() {
      this.updatingMarkerTargets = true;
      setTimeout(() => {
        // [WARNING] Please change me this is just no please.
        this.updatingMarkerTargets = false;
      }, 1500);
      await this.$store.dispatch('modifyAvailableMarkers', this.markerList).then(() => {
        this.$store.dispatch('getAvailableMarkers');
      })
      
    }
  },

  computed: {
    rows() {
      if (this.markerList.length > 0) {
        return this.markerList.length
      }
      else return 1
    },

    availableMarkers() {
      return this.$store.getters.availableMarkers
    },

    targetGroups() {
      return this.$store.getters.targetGroups;
    },

    targetGroupOptions() {
      if (this.targetGroups) {
        return [{'text': 'Select group', 'value': null }, ...this.targetGroups.map(t => { return { "text": t.name, "value": t.id }})]
      }
      else return [ {'text': 'No Groups Available', 'value': null} ]
    }
  },

  watch: {
    availableMarkers() {
      this.markerList = [...this.availableMarkers]
    }
  }
};
</script>


<style lang='scss' scoped>
.no-targets {
  font-size: 1.3rem;
  font-weight: 300;
  margin-top: 15px;
}
</style>