<template>
  <div class="mt-1" height="300px">
    <div class="mb-1">
      <b-form-input v-model="filter" placeholder="Filter samples" class="text-center"></b-form-input>
    </div>
    <div class="sample-list">
      <b-row v-for="sample in filteredSamples" :key="sample.id" class="my-0">
        <b-col>
          <b-button
            class="py-2 mt-1 bg-secondary text-light border"
            block
            @click="selectSample(sample.id)"
          >
            {{ sample.sample | shortName }}
          </b-button>
        </b-col>
      </b-row>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      filter: null,
    };
  },

  methods: {
    selectSample(id) {
      this.$store.dispatch("selectSample", id).then(
      );
    }
  },

  computed: {
    currentSamples() {
      return this.$store.getters.currentSamples;
    },

    filteredSamples() {
      return this.$store.getters.filteredSamples;
    },

    searchFilter() {
      if (this.filter == "") return null;
      else return this.filter;
    }
  },

  watch: {
    filteredSamples() {
      if (this.filteredSamples == null) return {};

      const firstSample = this.filteredSamples.slice(0, 1);
      this.selectSample(firstSample[0].id);
    },
    
    searchFilter() {
      this.$store.dispatch("filterSamples", this.filter);
    }
  }
};
</script>

<style lang='scss' scoped>
$GreyDarker: #505050;

.sample-list {
  height: 280px;
  width: 100%;
  overflow-y: scroll;
  -ms-overflow-style: none;

  &::-webkit-scrollbar {
    display: none;
  }

  -webkit-transition: all 0.1s ease-in-out;
  -moz-transition: all 0.1s ease-in-out;
  -ms-transition: all 0.1s ease-in-out;
  -o-transition: all 0.1s ease-in-out;
  transition: all 0.1s ease-in-out;
}

.no-projects {
  text-align: center;
  font-size: 1.2rem;
  font-weight: 500;
  padding-top: 100%;
}
</style>