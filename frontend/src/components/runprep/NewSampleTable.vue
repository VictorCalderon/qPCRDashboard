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
    </b-table>
  </div>
</template>

<script>
export default {
  data() {
    return {
      priorityOptions: [
        { text: "Standard", value: 0 },
        { text: "Urgent", value: 1 },
      ],

      sexOptions: [
        { text: "Choose", value: null },
        { text: "Male", value: 1 },
        { text: "Female", value: 0 },
      ],

      fields: [
        { key: 'well'},
        { key: "name" },
        { key: "cedula" },
        { key: "sex" },
        { key: "age" },
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