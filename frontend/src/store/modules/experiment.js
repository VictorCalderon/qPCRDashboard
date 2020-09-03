// import axios from 'axios'
import Vue from 'vue'
import Axios from 'axios';

const state = {
  samplePlate: [],

  priorityOptions: [
    { text: "Standard", value: 0 },
    { text: "Urgent", value: 1 },
  ],

  stepOptions: [
    { text: 'Rejected', value: 99 },
    { text: 'Received', value: 0 },
    { text: 'Extracted', value: 1 },
    { text: 'Amplified', value: 2 },
    { text: 'Reported', value: 3 },
  ],

  sexOptions: [
    { text: "Choose", value: null },
    { text: "Male", value: 1 },
    { text: "Female", value: 0 },
  ],
}

const mutations = {

  ADD_NEW_SAMPLE(state, sample) {

    // Copy old samples to new array
    let samples = [...state.samplePlate];

    // Push new sample to stack
    samples.push(sample);

    // Set new samples as variable
    Vue.set(state, 'samplePlate', samples)
  },

  PATIENTS_UPDATE_MSG(state, patientUpdateMessage) {

    // Set message
    Vue.set(state, 'patientMessage', patientUpdateMessage)
  }
}

const actions = {
  pushNewSample({ commit }, sample) {
    commit('ADD_NEW_SAMPLE', sample)
  },

  saveSamplePlate({ commit, getters }) {
    Axios.post('api/v1/patients', getters.samplePlate).then((res) => {
      commit('PATIENTS_UPDATE_MSG', res.data.msg)
    })
  }
}


const getters = {
  newSamplePlate(state) {
    return state.samplePlate || []
  },

  priorityOptions(state) {
    return state.priorityOptions
  },

  stepOptions(state) {
    return state.stepOptions
  },

  sexOptions(state) {
    return state.sexOptions
  }
}


export default {
  state,
  mutations,
  actions,
  getters
}