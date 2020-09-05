// import axios from 'axios'
import Vue from 'vue'
import Axios from 'axios';

const state = {}

const mutations = {

  LOAD_EXPERIMENTS(state, experiments) {
    Vue.set(state, 'loadedExperiments', experiments)
  },

  LOAD_NEXT_EXPERIMENTS(state, nextUrl) {
    Vue.set(state, 'next', nextUrl)
  },

  LOAD_PREV_EXPERIMENTS(state, prevUrl) {
    Vue.set(state, 'prev', prevUrl)
  },

  SELECT_EXPERIMENT(state, experiment) {
    Vue.set(state, 'currentExperiment', experiment)
  },

  // ADD_NEW_SAMPLE(state, sample) {
  //   // Copy old samples to new array
  //   let samples = [...state.samplePlate];

  //   // Push new sample to stack
  //   samples.push(sample);

  //   // Set new samples as variable
  //   Vue.set(state, 'samplePlate', samples)
  // },
}

const actions = {
  // pushNewSample({ commit }, sample) {
  //   commit('ADD_NEW_SAMPLE', sample)
  // },

  // saveSamplePlate({ commit, getters }) {
  //   Axios.post('api/v1/patients', getters.samplePlate).then((res) => {
  //     commit('PATIENTS_UPDATE_MSG', res.data.msg)
  //   })
  // },

  selectExperiment({ commit }, experiment) {
    commit('SELECT_EXPERIMENT', experiment);
},

  addNewExperiment({ commit }, newExperiment) {
    Axios.post('api/v1/experiments', newExperiment).then(
      res => {
        commit('SELECT_EXPERIMENT', res.data.experiment)
      }
    )
  },

  loadOldExperiments({ commit }) {
    Axios.get('api/v1/experiments', {
    }).then(res => {
      if (res.data.results.length > 0) {
        commit('LOAD_EXPERIMENTS', res.data.results);
        commit('LOAD_NEXT_EXPERIMENTS', res.data.next);
        commit('LOAD_PREV_EXPERIMENTS', res.data.prev);
      }
    })
  },
}


const getters = {
  newSamplePlate(state) {
    return state.samplePlate || []
  },

  loadedExperiments(state) {
    return state.loadedExperiments
  }
}


export default {
  state,
  mutations,
  actions,
  getters
}