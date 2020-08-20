<template>
  <b-card
    bg-variant="light"
    align="center"
    header="Sample Location Schema"
    header-bg-variant="dark"
    header-text-variant="white"
    class="m-2"
    v-if="sampleLocationSchemas"
  >
    <b-tooltip target="add-schema" triggers="hover" placement="right" variant="info">
      Schema keys can be alpha-numerical and must be present in each sample's name
      <br />e.g.: Sample-001-01 will be set as taken from Site A
    </b-tooltip>
    <template v-slot:header>
      <b-form-row class="justify-content-center mb-0">
        <b-col cols="8" offset="1">
          <h6 class="mb-0 mt-2">Sample Location Schema</h6>
        </b-col>
        <b-col cols="2" class="ml-auto" v-if="!visible">
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
        <b-col cols="2" class="ml-auto" v-if="visible">
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
      </b-form-row>
    </template>
    <b-collapse id="schema-form" v-model="visible">
      <b-form-row class="justify-content-center">
        <b-col cols="2" class="my-1">
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
            type="number"
          ></b-form-input>
        </b-col>
        <b-col cols="3" class="my-1">
          <label for="location-longitude">Longitude</label>
          <b-form-input
            type="number"
            id="location-longitude"
            aria-label="Longitude"
            placeholder="0.1874"
            v-model="newSchema.longitude"
            class="text-center"
            size="sm"
          ></b-form-input>
        </b-col>
        <b-col sm="12" lg="1" class="mt-1">
          <label for="location-color" class>Color</label>
          <b-form-input
            type="color"
            id="location-color"
            aria-label="Color"
            placeholder="#FFFFFF0"
            v-model="newSchema.color"
            class="text-center"
            size="sm"
          ></b-form-input>
        </b-col>
      </b-form-row>
      <b-form-row class="justify-content-center">
        <b-col cols="2">
          <label for="secret-text" class="text-light">Save</label>
          <b-button
            block
            class="px-1"
            size="md"
            variant="info"
            id="secret-text"
            @click="saveSchema"
            :disabled="!formReady"
          >
            <i class="fas fa-save"></i>
          </b-button>
        </b-col>
        <b-col cols="2">
          <label for="cancel-schema" class="text-light">Cancel</label>
          <b-button
            block
            class="px-1"
            size="md"
            variant="warning"
            id="cancel-schema"
            @click="toggleAddSchema"
          >
            <i class="fas fa-window-close"></i>
          </b-button>
        </b-col>
        <b-col cols="12">
          <hr />
        </b-col>
      </b-form-row>
    </b-collapse>

    <b-form-row v-if="schemas.length > 0" class="justify-content-center">
      <b-col>
        <b-table
          borderless
          selectable
          hover
          :fields="fields"
          :items="schemas"
          responsive="sm"
          select-mode="single"
          @row-selected="onRowSelected"
        >
          <template v-slot:cell(color)="data">
            <b :style="{color: data.item.color }">{{ data.item.color.toUpperCase() }}</b>
          </template>
        </b-table>
      </b-col>
    </b-form-row>

    <b-form-row v-if="noSchemasMessage">
      <b-col cols="12">
        <p class="no-map-schemas">Click on the plus button to add sampling sites</p>
      </b-col>
    </b-form-row>

    <template v-slot:footer v-if="schemas.length > 0">
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
        </b-col>
        <b-col cols="2">
          <b-button
            class="px-1"
            id="delete-schema"
            block
            variant="danger"
            @click="deleteSchema"
            :disabled="!selectedSchema"
            size="md"
          >
            <i class="fas fa-trash"></i>
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
      fields: ["key", "location", "latitude", "longitude", "color"],
      selectedSchema: null,
      newSchema: {
        key: null,
        location: null,
        latitude: null,
        longitude: null,
        color: "#FFFFFF"
      },
      schemas: []
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
      this.cleanSchemaForm();
    },

    cleanSchemaForm() {
      // Clear key
      this.newSchema.key = null;

      // Clear location
      this.newSchema.location = null;

      // Clear location
      this.newSchema.latitude = null;

      // Clear location
      this.newSchema.longitude = null;

      // Clear color
      this.newSchema.color = null;

      // Clear id
      this.newSchema.id = null;
    },

    toggleModifySchema() {
      // Set current select item as the item
      this.newSchema = { ...this.selectedSchema };

      // Toggle the modification collapse
      this.visible = true;
      this.modification = true;
    },
    deleteSchema() {
      this.$store
        .dispatch("deleteSampleLocationSchema", this.selectedSchema.id)
        .then(() => {
          this.loadSchemas();
        });
    },

    toggleAddSchema() {
      // Clean schemas
      this.cleanSchemaForm();

      // Toggle add schemas
      this.modification = false;
      this.visible = !this.visible;
    },

    saveSchema() {
      const newSchema = { ...this.newSchema };
      this.$store
        .dispatch("updateSampleLocationSchemas", newSchema)
        .then(() => {
          this.toggleAddSchema();
        })
        .then(() => {
          this.loadSchemas();
        });
    },

    async loadSchemas() {
      await this.$store.dispatch("getSampleLocationSchemas").then(() => {
        // this.schemas = [...this.sampleLocationSchemas];
      });
    }
  },

  computed: {
    noSchemasMessage() {
      return this.schemas.length == 0 & !this.visible & !this.modification
    },

    sampleLocationSchemas() {
      return this.$store.getters.sampleLocationSchemas;
    },

    disableAddSchema() {
      if (this.newSchema) {
        return false;
      } else return true;
    },

    formReady() {
      if (
        this.newSchema.key &&
        this.newSchema.location &&
        this.newSchema.latitude &&
        this.newSchema.longitude &&
        this.newSchema.color
      ) {
        return true;
      } else return false;
    }
  },

  async mounted() {
    // Get schemas
    this.loadSchemas();
  },

  watch: {
    sampleLocationSchemas() {
      this.schemas = [...this.sampleLocationSchemas];
    },

    selectedSchema() {
      this.newSchema = { ...this.selectedSchema };
    }
  }
};
</script>

<style lang='scss' scoped>
.no-map-schemas {
  font-size: 1.5rem;
  font-weight: 300;
  margin-top: 15px;
}
</style>