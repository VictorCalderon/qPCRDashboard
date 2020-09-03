<template>
  <div>
    <b-table
      striped
      class="text-center"
      scrollable
      hover
      :items="currentExperimentPlate"
      :fields="fields"
    >
    
      <template v-slot:cell(sex)="data">
        <span>{{ sexOptions.find(s => s.value == data.item.sex)['text'] }}</span>
      </template>

      <template v-slot:cell(priority)="data">
        <span
          :style="{color: data.item.priority == 0 ? '#36382E' : '#296EB4'}"
        >{{ priorityOptions.find(p => p.value == data.item.priority)['text'] }}</span>
      </template>

      <template v-slot:cell(geoZone)="data" v-if="availableGeoZones">
        <span>{{ availableGeoZones.find(g => g.value == data.item.geoZone)['text'] }}</span>
      </template>

      <template v-slot:cell(step)="data" v-if="stepOptions">
        <b
         :style="{color: data.item.step == 99 ? '	#FF9900' : '#393E41'}"
        >{{ stepOptions.find(s => s.value == data.item.step)['text'] }}</b>
      </template>
    </b-table>
  </div>
</template>

<script>

export default {
  data() {
    return {
      fields: [
        { key: 'well'},
        { key: "name" },
        { key: "barcode" },
        { key: "cedula" },
        { key: "sex" },
        { key: "birthDate" },
        { key: "priority" },
        // { key: "description" },
        { key: "geoZone" },
        { key: "step" },
      ],
    };
  },

  computed: {
    currentExperimentPlate() {
      return this.$store.getters.newSamplePlate;
    },
  
    sampleLocationSchemas() {
      return this.$store.getters.sampleLocationSchemas;
    },

    stepOptions() {
      return this.$store.getters.stepOptions
    },

    sexOptions() {
      return this.$store.getters.sexOptions
    },

    priorityOptions() {
      return this.$store.getters.priorityOptions
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
  },
};
</script>