// import axios from 'axios'
import Vue from 'vue'

const state = {
  newSamplePlate: [],

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
    let samples = [...state.newSamplePlate];

    // Push new sample to stack
    samples.push(sample);

    // Set new samples as variable
    Vue.set(state, 'newSamplePlate', samples)
  }
}

const actions = {
  pushNewSample({ commit }, sample) {
    commit('ADD_NEW_SAMPLE', sample)
  }
}


const getters = {
  newSamplePlate(state) {
    return state.newSamplePlate || []
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