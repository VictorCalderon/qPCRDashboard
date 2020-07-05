<template>
  <b-card
    bg-variant="light"
    align="center"
    header="Sample Location Schema"
    header-bg-variant="dark"
    header-text-variant="white"
    class="m-2"
  >
    <b-tooltip target="add-schema" triggers="hover" placement="right" variant="info">
      Schema keys can be alpha-numerical and must be present in each sample's name
      <br />e.g.: Sample-001-01 will be set as taken from Site A
    </b-tooltip>
    <template v-slot:header>
      <b-form-row class="justify-content-center mb-0">
        <b-col cols="8" offset="2">
          <h6 class="mb-0 mt-2">Sample Location Schema</h6>
        </b-col>
        <b-col cols="1" class="ml-auto">
          <b-button
            id="add-schema"
            block
            variant="secondary"
            :disabled="disableAddSchema"
            @click="toggleAddSchema"
            size="sm"
            class="px-1"
            v-if="visible"
          >
            <i class="fas fa-minus-square"></i>
          </b-button>
        </b-col>
        <b-col cols="1" class="ml-auto">
          <b-button
            id="add-schema"
            block
            variant="secondary"
            :disabled="disableAddSchema"
            @click="toggleAddSchema"
            size="sm"
            class="px-1"
          >
            <i class="fas fa-plus-square"></i>
          </b-button>
        </b-col>
      </b-form-row>
    </template>
    <b-collapse id="schema-form" v-model="visible">
      <b-form-row class="justify-content-center">
        <b-col cols="3" class="my-1">
          <label for="location-key">Key</label>
          <b-form-input
            id="location-key"
            aria-label="Key"
            placeholder="001"
            v-model="newSchema.key"
            class="text-center"
            size="sm"
          ></b-form-input>
        </b-col>
        <b-col cols="3" class="my-1">
          <label for="location-name">Name</label>
          <b-form-input
            id="location-name"
            aria-label="LocationName"
            placeholder="Site A"
            v-model="newSchema.location"
            class="text-center"
            size="sm"
          ></b-form-input>
        </b-col>
        <b-col cols="3" class="my-1">
          <label for="location-latitude">Latitude</label>
          <b-form-input
            id="location-latitude"
            aria-label="Latitude"
            placeholder="52.0794"
            v-model="newSchema.latitude"
            class="text-center"
            size="sm"
          ></b-form-input>
        </b-col>
        <b-col cols="3" class="my-1">
          <label for="location-longitude">Longitude</label>
          <b-form-input
            id="location-longitude"
            aria-label="Longitude"
            placeholder="0.1874"
            v-model="newSchema.longitude"
            class="text-center"
            size="sm"
          ></b-form-input>
        </b-col>
      </b-form-row>
      <b-button
        v-if="!modification"
        class="mt-3"
        size="sm"
        variant="success"
        @click="addSchema"
      >Add Schema</b-button>
      <b-button
        v-if="modification"
        class="mt-3 mx-2"
        size="sm"
        variant="secondary"
        @click="modifySchema"
      >Cancel</b-button>
      <hr class="my-3" />
    </b-collapse>

    <b-row v-if="schemas.length > 0" class="justify-content-center">
      <b-col>
        <b-table
          hover
          :items="schemas"
          borderless
          selectable
          @row-selected="onRowSelected"
          responsive="sm"
          select-mode="single"
          :fields="fields"
        ></b-table>
      </b-col>
    </b-row>
    <template v-slot:footer>
      <b-form-row class="justify-content-end">
        <b-col cols="2">
          <b-button
            id="modify-schema"
            class="px-1"
            block
            variant="warning"
            @click="toggleModifySchema"
            :disabled="!selectedSchema"
            size="md"
            v-if="!modification"
          >
            <i class="fas fa-edit"></i>
          </b-button>
          <b-button
            id="modify-schema"
            class="px-1"
            block
            variant="success"
            @click="modifySchema"
            :disabled="!selectedSchema"
            size="md"
            v-if="modification"
          >
            <i class="fas fa-check-square"></i>
          </b-button>
        </b-col>
        <b-col cols="2">
          <b-button
            class="px-1"
            id="delete-schema"
            block
            variant="danger"
            @click="removeSchema"
            :disabled="!selectedSchema"
            size="md"
          >
            <i class="fas fa-trash"></i>
          </b-button>
        </b-col>
        <b-col cols="2">
          <b-button
            id="save-schemas"
            block
            variant="info"
            @click="saveSchemas"
            class="px-1"
            size="md"
          >
            <i class="fas fa-save"></i>
          </b-button>
        </b-col>
      </b-form-row>
    </template>
  </b-card>
</template>

<script>
export default {
  data() {
    return {
      visible: false,
      modification: false,
      fields: ["key", "location", "latitude", "longitude"],
      selectedSchema: null,
      newSchema: {
        id: null,
        key: null,
        location: null,
        latitude: null,
        longitude: null
      },
      schemas: [
        {
          id: 0,
          key: "001",
          location: "Sede Central",
          latitude: "18.4358",
          longitude: "-69.9853"
        },
        {
          id: 1,
          key: "002",
          location: "Piantini",
          latitude: "18.4772",
          longitude: "-69.9263"
        },
        {
          id: 2,
          key: "003",
          location: "Santiago",
          latitude: "19.4548",
          longitude: "-70.6929"
        }
      ]
    };
  },
  methods: {
    toggleCollapse() {
      this.visible = !this.visible;
    },

    onRowSelected(items) {
      this.selectedSchema = items[0];
    },

    addSchema() {
      // Check if schema is present
      const key = this.schemas.filter(s => s.key == this.newSchema.key);
      const location = this.schemas.filter(
        l => l.location == this.newSchema.location
      );

      // Add if condition is met
      if (key.length > 0 || location.length > 0) {
        alert("Key or Location already in use!");
      }

      // Add schema and clear inputs
      else this.schemas.push({ ...this.newSchema });

      // Clear schema
      this.cleanSchema();
    },

    cleanSchema() {
      // Add key
      this.newSchema.key = null;

      // Add location
      this.newSchema.location = null;

      // Add location
      this.newSchema.latitude = null;

      // Add location
      this.newSchema.longitude = null;
    },

    removeSchema() {
      const deleteIndex = this.schemas.findIndex(
        s => s.key == this.selectedSchema.key
      );
      this.schemas.splice(deleteIndex, 1);
    },

    toggleModifySchema() {
      // Set current select item as the item
      this.newSchema = { ...this.selectedSchema };

      // Toggle the modification collapse
      this.visible = true;
      this.modification = true;
    },

    modifySchema() {
      // Find id
      const schemaID = this.schemas.findIndex(s => s.id == this.newSchema.id);

      // Set new schema
      this.schemas[schemaID].key = this.newSchema.key;
      this.schemas[schemaID].name = this.newSchema.name;
      this.schemas[schemaID].latitude = this.newSchema.latitude;
      this.schemas[schemaID].longitude = this.newSchema.longitude;

      // Set modification layout
      this.toggleCollapse();
      this.modification = !this.modification;

      //
    },

    toggleAddSchema() {
      // Clean schemas
      this.cleanSchema();

      // Toggle add schemas
      this.modification = false;
      this.visible = !this.visible;
    },

    saveSchemas() {
      console.log("Implement me please");
    }
  },
  computed: {
    disableAddSchema() {
      if (this.newSchema) {
        return false;
      } else return true;
    }
  }
};
</script>

<style>
</style>