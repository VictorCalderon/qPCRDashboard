<template>
  <b-container fluid>
    <b-form-row>
      <!-- <b-col cols="12" class="text-center">
        <h5>Patient Data</h5>
      </b-col> -->
    </b-form-row>
    <b-form-row class="mt-3">
      <b-col cols="4" md="4" sm="12">
        <b-form-group id="cedula-input" description="Cedula">
          <b-form-input
            class="text-center text-muted"
            placeholder="___-_______-_"
            v-model="patient.cedula"
          ></b-form-input>
        </b-form-group>
      </b-col>
      <b-col cols="8">
        <b-form-group id="name-input" description="Patient Name">
          <b-form-input
            class="text-center text-muted"
            placeholder="Enter patient name"
            v-model="patient.name"
          ></b-form-input>
        </b-form-group>
      </b-col>
    </b-form-row>
    <b-form-row>
      <b-col cols="3" md="3" sm="12" offset=2>
        <b-form-group id="sex-select" description="Sex">
          <b-form-select v-model="patient.sex" :options="sexOptions"></b-form-select>
        </b-form-group>
      </b-col>
      <b-col cols="5" md="5" sm="12">
        <b-form-group id="age-input" description="BirthDate">
          <b-form-input v-model="patient.birthDate" type="date" class="text-center text-muted"></b-form-input>
        </b-form-group>
      </b-col>
    </b-form-row>
    <b-form-row>
      <b-col cols="12">
        <hr />
      </b-col>
      <!-- <b-col cols="12" class="text-center">
        <h5>Sample Data</h5>
      </b-col> -->
      <b-col cols="4" md="4" sm="12">
        <b-form-group id="barcode-input" description="Barcode">
          <b-form-input class="text-center text-muted" placeholder="Scan" v-model="sample.barcode"></b-form-input>
        </b-form-group>
      </b-col>
      <b-col cols="4" md="4" sm="12">
        <b-form-group id="collection-date-input" description="Collection Date">
          <b-form-input class="text-center text-muted" type="date" v-model="sample.collectionDate"></b-form-input>
        </b-form-group>
      </b-col>
      <b-col cols="4" md="4" sm="12">
        <b-form-group id="priority-select" description="Priority Level">
          <b-form-select v-model="sample.priority" :options="priorityOptions" class="text-center"></b-form-select>
        </b-form-group>
      </b-col>
      <b-col cols="5">
        <b-form-group id="loc-input" description="Geo Zone">
          <b-form-select
            class="text-center text-muted"
            placeholder="GeoZone"
            v-model="sample.geoZone"
            :options="availableGeoZones"
          ></b-form-select>
        </b-form-group>
      </b-col>
      <b-col cols="7">
        <b-form-group id="description-textarea" description="Sample description">
          <b-form-input
            id="description-input"
            placeholder="Patient's anamnesis can be used."
            v-model="sample.description"
            class="text-center"
          ></b-form-input>
        </b-form-group>
      </b-col>
    </b-form-row>
    <b-form-row></b-form-row>
    <hr />
    <b-form-row>
      <b-col cols="4" offset="2">
        <b-button
          class="mx-1 my-2 btn-success btn-block"
          @click="addNewSample"
          :disabled="fullPlate || sampleFormReady"
        >Commit change</b-button>
      </b-col>
      <b-col cols="3">
        <b-button
          class="mx-1 my-2 btn-info btn-block"
          @click="wellSkip++"
          :disabled="fullPlate"
        >Skip Well</b-button>
      </b-col>
    </b-form-row>
  </b-container>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  data() {
    return {
      wellSkip: 0,
      patient: {
        name: null,
        cedula: null,
        sex: 1,
        birthDate: null,
        step: 0,
      },

      sample: {
        barcode: null,
        collectionDate: null,
        priority: 0,
        description: null,
        geoZone: 1,
      }
    };
  },

  computed: {
    ...mapGetters(['priorityOptions', 'sexOptions', 'sampleLocationSchemas', 'currentExperiment']),
    
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
      return this.currentSamplePlate.length + this.wellSkip == 96;
    },

    sampleFormReady() {
      if (
        this.sample.barcode &&
        this.patient.name &&
        this.patient.birthDate &&
        this.sample.collectionDate &&
        this.sample.geoZone
      ) {
        return false;
      } else return true;
    },

    currentSamplePlate() {
      return this.$store.getters.newSamplePlate || [];
    },

    plateWells() {
      // Basic
      const cols = ["A", "B", "C", "D", "E", "F", "G", "H"];

      // Iterate over it
      let wells = [];

      for (let i = 1; i < 13; i++) {
        for (let j = 0; j < 8; j++) {
          wells.push(cols[j] + i);
        }
      }

      return wells;
    },

    nextWell() {
      // Generate next well
      return this.plateWells[this.currentSamplePlate.length + this.wellSkip];
    },
  },

  methods: {
    async loadSchemas() {
      await this.$store.dispatch("getSampleLocationSchemas");
    },

    addNewPatient() {
      this.$store.dispatch('addOrModifyPatient', 
      {
        'full_name': this.patient.name,
        'cedula': this.patient.cedula,
        'birth_date': this.patient.birthDate,
        'is_male': this.patient.sex }
      );
    },

    addNewSample() {
      this.$store.dispatch('addNewSample', 
      {
        'sample': this.sample.barcode,
        'tmpl_well': this.nextWell,
        'priority_level': this.sample.priority,
        'collection_date': this.sample.collectionDate,
        'description': this.sample.description,
        'location_id': this.sample.geoZone,
        'patient_id': this.patient.id,
        'experiment_id': this.currentExperiment.id
      })
    },

    addPatientSample() {
      // Add patient
      this.addNewPatient;

      // Add sample after patient
      this.addNewSample;

      // Clean sample form after adding sample
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
        step: 1,
        collectionDate: null,
      };
    },
  },

  mounted() {
    this.loadSchemas();
  },
};
</script>

<style>
</style>