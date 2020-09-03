// import axios from 'axios'
import Vue from 'vue'

const state = {
  newSamplePlate: [],
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
  }
}


export default {
  state,
  mutations,
  actions,
  getters
}