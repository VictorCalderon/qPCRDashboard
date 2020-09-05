import Vue from 'vue'
import Axios from 'axios'

const state = {

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
    { text: "Male", value: true },
    { text: "Female", value: false },
  ],
}

const mutations = {
  PATIENT_UPDATE_MSG(state, msg) {
    Vue.set(state, 'patientMessage', msg)
  },

  SET_CURRENT_PATIENT(state, patient) {
    Vue.set(state, 'currentPatient', patient)
  }
}

const actions = {

  addOrModifyPatient({ commit }, patient) {
    Axios.post('/api/v1/patients', patient)
      .then(res => { 
        commit('SET_CURRENT_PATIENT', res.data.patient);
        commit('PATIENT_UPDATE_MSG', res.data.msg);
      })
      .catch(res => { commit('PATIENT_UPDATE_MSG', res.data.msg) })
  }
}


const getters = {

  priorityOptions(state) {
    return state.priorityOptions
  },

  stepOptions(state) {
    return state.stepOptions
  },

  sexOptions(state) {
    return state.sexOptions
  },
}


export default {
  state,
  mutations,
  actions,
  getters
}