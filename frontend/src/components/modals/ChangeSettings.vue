<template>
  <BaseModal id="modal">
    <template v-slot:header class="modal-header">
      <div class="upper-header">
        <span aria-hidden="true" @click="toggleChangeSettings">&times;</span>
      </div>
      <h2 class="modal-title">
        <i class="fa fa-cogs"></i>&nbsp;Settings
      </h2>
      <hr />
    </template>
    <template v-slot:body class="modal-body">
      <h3 class="custom-settings-title">Custom Labels</h3>
      <p class="custom-settings-description">These will be used to classify your data.</p>
      <div class="custom-labels">
        <input
          v-for="(label, i) in Labels"
          :key="i"
          type="text"
          v-model="newLabels[i]"
          :placeholder="label"
        />
      </div>
      <hr />
      <div class="export-settings-hub">
        <h3 class="custom-settings-title">Export Settings</h3>
        <p class="custom-settings-description">These will be used to export your classified data.</p>
        <div class="custom-exports">
          <input
            type="text"
            v-model="newExport.export_name"
            :placeholder="customExports.export_name"
          />
          <button
            @click="setExportSep(',')"
            :class="[activeSeparator ? 'settings-active' : '']"
          >Comma</button>
          <button
            @click="setExportSep('\t')"
            :class="[!activeSeparator ? 'settings-active' : '']"
          >Tab</button>
        </div>
        <hr />
      </div>
    </template>
    <template v-slot:footer class="modal-footer">
      <div>
        <button class="custom-confirm" @click="confirmChanges">Confirm changes</button>
        <br />
      </div>
    </template>
  </BaseModal>
</template>

<script>
import BaseModal from "@/components/modals/BaseModal";

export default {
  components: {
    BaseModal
  },
  data() {
    return {
      newLabels: [null, null, null, null],
      newExport: {
        export_name: null,
        export_sep: null
      }
    };
  },
  methods: {
    setAsNullIfEmpty(value) {
      if (value == "") null;
      else return value;
    },

    toggleChangeSettings() {
      this.$store.dispatch("toggleSettingsModal");
    },

    setExportSep(sep) {
      this.newExport.export_sep = sep;
    },

    confirmChanges() {
      // Confirm label changes
      const cleanArray = this.newLabels.map((label, i) => {
        if (label == "" || label == null) {
          return this.Labels[i];
        } else return label;
      });

      this.$store.dispatch("changeLabels", cleanArray);
    }
  },
  computed: {
    // customLabels() {
    //   return this.$store.getters.customLabels;
    // },

    Labels() {
      return this.$store.getters.customLabels;
    },

    customExports() {
      return this.$store.getters.customExports;
    },

    activeSeparator() {
      const is_comma = this.customExports.export_sep == ",";
      return is_comma ? true : false;
    }
  },
  watch: {}
};
</script>

<style lang='scss' scoped>
$Indicator: #0976be;
$GreyDarker: #636262;
$GreyLighter: #d6d6d6;
$IndicatorLight: #7dbaf3;

#modal {
  position: absolute;
  top: 15%;
  left: 25%;
  height: 60%;
  width: 50%;
  background: none;

  .modal-header {
    display: block;

    .upper-header {
      height: 5px;

      span {
        display: block;
        position: relative;
        float: right;
        right: 10px;
        font-size: 1.8rem;
        cursor: pointer;

        &:hover {
          color: rgb(190, 24, 24);
        }
      }
    }

    .post-message {
      text-align: center;
      color: $Indicator;
      font-weight: 300;
      font-size: 1.5rem;
    }

    .modal-title {
      display: block;
      text-align: center;
      font-size: 2rem;
      font-weight: 300;
      padding: 0px 0;

      .fas {
        position: relative;
        color: $GreyDarker;
        margin-right: 10px;
        font-size: 1.4rem;
      }
    }
  }

  .modal-body {
    input {
      color: black;
      font-size: 1.2rem;
      text-align: center;
      margin: 5px;
      border-radius: 5px;
      padding: 10px;
      border: 1px solid $GreyDarker;
    }

    button {
      color: $GreyDarker;
      font-size: 1.2rem;
      text-align: center;
      margin: 5px;
      border-radius: 5px;
      padding: 10px;
      border: 1px solid $GreyDarker;
      cursor: pointer;
    }

    .settings-active {
      background: $GreyDarker;
      color: white;
    }

    input[type="checkbox"] {
      -webkit-appearance: none;
      position: relative;
      top: 15px;
      // left: 60px;
      width: 20px;
      height: 20px;
      background: white;
      border-radius: 5px;
      border: 2px solid #555;
    }

    input[type="checkbox"]:checked {
      background: $Indicator;
    }

    .custom-settings-title {
      text-align: center;
      font-weight: 500;
      font-size: 1.3rem;
      margin-bottom: -10px;
    }

    .custom-settings-description {
      text-align: center;
      font-weight: 300;
      font-size: 1.1rem;
      padding: none;
    }

    .custom-labels {
      display: grid;
      margin: 10px 20px 20px 20px;
      grid-template-columns: repeat(2, 1fr);
      grid-template-rows: repeat(2, 1fr);
    }

    .custom-exports {
      display: grid;
      margin: 10px 20px 20px 20px;
      grid-template-columns: 50% 25% 25%;
    }
  }

  .modal-footer {
    .custom-confirm {
      background: none;
      color: $GreyDarker;
      border: none;
      padding: 10px 15px;
      border-radius: 5px;
      margin: 0% 32.5% 3% 32.5%;
      text-transform: uppercase;
      font-family: Verdana, Geneva, Tahoma, sans-serif;
      font-size: 1.1rem;
      box-shadow: 0 10px 30px 0 #8b949965;
      -webkit-box-shadow: 0 10px 30px 0 #8b949965;
      -webkit-transition: all 0.2s ease-in-out;
      -webkit-border-radius: 5px;
      -moz-transition: all 0.2s ease-in-out;
      -ms-transition: all 0.2s ease-in-out;
      -o-transition: all 0.2s ease-in-out;
      transition: all 0.2s ease-in-out;
      cursor: pointer;

      &:active {
        -moz-transform: scale(0.9);
        -webkit-transform: scale(0.9);
        -o-transform: scale(0.9);
        -ms-transform: scale(0.9);
        transform: scale(0.9);
      }

      .fas {
        font-size: 1.2rem;
        color: $IndicatorLight;
      }

      &:hover {
        background: $GreyDarker;
        color: white;
      }
    }
  }

  .no-projects {
    font-size: 1.2rem;
    text-align: center;
    padding-bottom: 10px;
    padding-top: 10px;
  }
}
</style>

