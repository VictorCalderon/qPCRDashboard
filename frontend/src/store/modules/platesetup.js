import axios from 'axios'
import Vue from 'vue'

const state = {
    currentPlate: null,
    currentPatient: null,
    currentSample: null
}

const mutations = {

    SET_CURRENT_PLATE(state, currentPlate) {
        Vue.set(state, 'currentPlate', currentPlate)
    },

    SET_CURRENT_PATIENT(state, currentPatient) {
        Vue.set(state, 'currentPatient', currentPatient)
    },

    SET_CURRENT_SAMPLE(state, currentSample) {
        Vue.set(state, 'currentSample', currentSample)
    }
}

const actions = {

    addNewExperiment({ commit }, newExperiment) {
        axios.post('api/v1/experiments', newExperiment).then(
            res => {
                commit('SET_CURRENT_PLATE', res.data)
            }
        )
    },

    addNewPatient({ commit }, newPatient) {
        axios.post('api/v1/patients', newPatient).then(
            res => {
                commit('SET_CURRENT_PATIENT', res.data)
            }
        )
    },

    updateBriefingData({ commit }) {
        axios.get('api/v1/dashboard/briefing').then(
            res => {
                commit('SET_BRIEFING_DATA', res.data)
            }
        )
    },
}


const getters = {
    currentPlate(state) {
        return state.currentPlate
    },

    currentPatient(state) {
        return state.currentPatient
    },

    currentSample() {
        return state.currentSample
    },
}


export default {
    state,
    mutations,
    actions,
    getters
}