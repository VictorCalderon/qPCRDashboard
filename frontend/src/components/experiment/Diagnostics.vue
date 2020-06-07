<template>
  <div>
    <b-row>
      <b-col v-for="(label, i) in customLabels" :key="i">
        <b-button
          :class="{current: label==result}"
          class="mt-3 py-2"
          variant="secondary"
          block
          size="sm"
          @click="updateSample(label)"
        >{{label}}</b-button>
      </b-col>
    </b-row>
  </div>
</template>

<script>
export default {
  data() {
    return {
      customLabel: "Etiqueta",
      result: null
    };
  },
  methods: {
    updateSample(result) {
      this.result = result;
      this.$store.dispatch("updateSample", result);
    }
  },
  computed: {
    currentSample() {
      if (this.$store.getters.currentSample == null) return {};
      return this.$store.getters.currentSample;
    },
    customLabels() {
      if (this.$store.getters.customLabels) {
        return this.$store.getters.customLabels;
      }
      return ["DETECTED", "NOT DETECTED", "UNDETERMINED", "RETAINED"];
    }
  },
  watch: {
    currentSample() {
      this.result = this.currentSample.result;
    }
  }
};
</script>

<style lang='scss' scoped>
$GreyLight: #d8d8d8;
$GreyDark: #969696;
$GreenRef: #00843d;
$GreenRefDark: #005c2b;
$GreenRefLight: #01a34d;
$GreyDarker: #505050;
$GreyBackground: #e6e6e6;
$GreyBackgroundDark: #535353;
$Indicator: #539ee4;

.project-control {
  display: grid;
  padding: 3px 0px;
  grid-template-columns: repeat(4, 25%);

  button {
    font-size: 0.8rem;
    font-weight: 500;
    margin: 5px;
    height: 35px;
    // width: 120px;
    border-radius: 10px;
    background: none;

    &:hover {
      cursor: pointer;
      background: $GreyDarker;
      color: white;
    }
  }

  .current {
    background: $GreyDarker;
    color: white;
  }

  .delete-button {
    background: rgb(241, 27, 27);
    color: white;
  }

  .export-button {
    background: rgb(28, 147, 245);
    color: white;
  }
}
</style>