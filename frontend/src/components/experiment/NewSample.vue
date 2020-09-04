<template>
  <b-container fluid>
    <b-form-row class="mt-1">
      <b-col cols="4" md="4" sm="12">
        <b-form-group id="cedula-input" description="Cedula">
          <b-form-input
            class="text-center text-muted"
            placeholder="___-_______-_"
            v-model="patient.cedula"
          ></b-form-input>
        </b-form-group>
      </b-col>
      <b-col cols="4" md="4" sm="12">
        <b-form-group id="barcode-input" description="Barcode">
          <b-form-input
            class="text-center text-muted"
            placeholder="Scan"
            v-model="patient.barcode"
          ></b-form-input>
        </b-form-group>
      </b-col>
      <b-col cols="4" md="4" sm="12">
        <b-form-group id="priority-select" description="Priority Level">
          <b-form-select v-model="patient.priority" :options="priorityOptions" class="text-center"></b-form-select>
        </b-form-group>
      </b-col>
    </b-form-row>
    <b-form-row>
      <b-col cols="12">
        <hr />
      </b-col>
      <b-col cols="7">
        <b-form-group id="name-input" description="Patient Name">
          <b-form-input
            class="text-center text-muted"
            placeholder="Enter patient name"
            v-model="patient.name"
          ></b-form-input>
        </b-form-group>
      </b-col>
      <b-col cols="5">
        <b-form-group id="loc-input" description="Geo Zone">
          <b-form-select
            class="text-center text-muted"
            placeholder="GeoZone"
            v-model="patient.geoZone"
            :options="availableGeoZones"
          ></b-form-select>
        </b-form-group>
      </b-col>
    </b-form-row>
    <b-form-row>
      <b-col cols="4" md="4" sm="12">
        <b-form-group id="suspected-input" description="Suspected Illness">
          <b-form-input
            class="text-center text-muted"
            placeholder="COVID-19"
            v-model="patient.suspected"
          ></b-form-input>
        </b-form-group>
      </b-col>
      <b-col cols="3" md="3" sm="12">
        <b-form-group id="sex-select" description="Sex">
          <b-form-select v-model="patient.sex" :options="sexOptions"></b-form-select>
        </b-form-group>
      </b-col>
      <b-col cols="5" md="5" sm="12">
        <b-form-group id="age-input" description="BirthDate">
          <b-form-input v-model="patient.birthDate" type="date"></b-form-input>
        </b-form-group>
      </b-col>
    </b-form-row>
    <b-form-row>
      <b-col cols="12">
        <b-form-group id="description-textarea" description="Sample description">
          <b-form-textarea
            id="description-textarea"
            placeholder="If available, the patient's anamnesis can be used."
            v-model="patient.description"
            class="text-center"
            size="sm"
          ></b-form-textarea>
        </b-form-group>
      </b-col>
    </b-form-row>
    <hr>
    <b-form-row >
      <b-col cols="5" offset=1>
        <b-button class="mx-1 my-2 btn-success btn-block" @click="pushNewSample" :disabled="fullPlate || sampleFormRead">Add Sample</b-button>
      </b-col>
      <b-col cols=4>
        <b-button class="mx-1 my-2 btn-info btn-block" @click="wellSkip++" :disabled="fullPlate">Skip</b-button>
      </b-col>
    </b-form-row>
  </b-container>
</template>

<script>
export default {
  data() {
    return {
      wellSkip: 0,
      patient: {
        name: null,
        cedula: null,
        barcode: null,
        sex: 1,
        birthDate: '1996-05-25',
        priority: 0,
        description: null,
        geoZone: 1,
        step: 0
      },
    };
  },

  computed: {
    priorityOptions() {
      return this.$store.getters.priorityOptions
    },

    sexOptions() {
      return this.$store.getters.sexOptions
    },

    availableGeoZones() {
      if (this.sampleLocationSchemas) {
        return [
          ...this.sampleLocationSchemas.map((loc) => {
            return {
              text: loc.location,
              value: loc.id,
            };
          }),
        ];
      } else return [{ text: "No Schema available", value: null }];
    },

    fullPlate() {
      return this.currentSamplePlate.length + this.wellSkip == 96
    },

    sampleFormRead() {
      if (
        this.patient.barcode 
        && this.patient.name && this.patient.birthDate 
        && this.patient.sex && this.patient.birthDate 
        && this.patient.geoZone) {
        return false
      }
      else return true
    },

    sampleLocationSchemas() {
      return this.$store.getters.sampleLocationSchemas;
    },

    currentSamplePlate() {
      return this.$store.getters.newSamplePlate || []
    },

    plateWells() {
      // Basic
      const cols = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'];

      // Iterate over it
      let wells = [];

      for (let i = 1; i < 13; i++) {
        for (let j = 0; j < 8; j++) {
          wells.push(cols[j] + i)
        }}
      
      return wells
    },

    nextWell() {
      // Generate next well
      return this.plateWells[this.currentSamplePlate.length + this.wellSkip]
    }
  },

  methods: {
    async loadSchemas() {
      await this.$store.dispatch("getSampleLocationSchemas");
    },

    pushNewSample() {
      let patient = {...this.patient, 'well': this.nextWell}
      this.$store.dispatch('pushNewSample', patient)
      this.cleanNewSampleForm()
    },

    cleanNewSampleForm() {
      this.patient = {
        well: "",
        name: "",
        cedula: "",
        sex: null,
        birthDate: null,
        priority: 0,
        description: "",
        geoZone: 0,
        step: 1
      }
    }
  },

  mounted() {
    this.loadSchemas();
  },
};
</script>

<style>
</style>