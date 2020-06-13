import axios from 'axios'
import Vue from 'vue'

const state = {}

const mutations = {
    'INIT_EXPERIMENTS'(state) {
        Vue.set(state, 'currentExperimentFile', null);
        Vue.set(state, 'allExperiments', null);
        Vue.set(state, 'queriedExperiments', []);
        Vue.set(state, 'currentExperiment', null);
        Vue.set(state, 'currentExperimentResults', null);
    },

    'LOAD_ALL_EXPERIMENTS'(state, experiments) {
        Vue.set(state, 'allExperiments', experiments)
    },

    'LOAD_NEXT_EXPERIMENTS'(state, nextUrl) {
        Vue.set(state, 'next', nextUrl)
    },

    'LOAD_PREV_EXPERIMENTS'(state, prevUrl) {
        Vue.set(state, 'prev', prevUrl)
    },

    'SELECT_EXPERIMENT'(state, experiment) {
        Vue.set(state, 'currentExperiment', experiment)
    },

    'UPDATE_MSG'(state, msg) {
        Vue.set(state, 'updateMsg', msg)
    },

    'EXPORT_EXPERIMENT_FILE'(state, file) {
        Vue.set(state, 'currentExperimentFile', file)
    },

    'CLEAR_EXPERIMENTS'(state) {
        Vue.set(state, 'allExperiments', [])
    },

    'EXPERIMENTS_QUERY'(state, experiments) {
        Vue.set(state, 'queriedExperiments', experiments)
    },

    'CLEAR_CURRENT_EXPERIMENT'(state) {
        Vue.set(state, 'currentExperiment', null)
    },

    'SET_EXPERIMENT_RESULTS'(state, results) {
        Vue.set(state, 'currentExperimentResults', results)
    },

    'AVAILABLE_MARKERS'(state, markers) {
        Vue.set(state, 'availableMarkers', markers)
    }
}

const actions = {
    initExperiments({ commit }) {
        commit('INIT_EXPERIMENTS')
    },

    loadExperiments({ commit }) {
        axios.get('api/v1/experiments', {
        }).then(res => {
            if (res.data.results.length > 0) {
                commit('LOAD_ALL_EXPERIMENTS', res.data.results);
                commit('LOAD_NEXT_EXPERIMENTS', res.data.next);
                commit('LOAD_PREV_EXPERIMENTS', res.data.prev);
            }
        })
    },

    async getMarkers({ commit }) {
        await axios.get("api/v1/markers").then(res => {
            commit('AVAILABLE_MARKERS', res.data.markers);
        });
    },

    loadCurrentExperimentResults({ commit, getters }) {
        axios.get(`api/v1/experiments/${getters.currentExperiment.id}/results`).then(res => {
            commit('SET_EXPERIMENT_RESULTS', res.data)
        })
    },

    selectExperiment({ commit }, experiment) {
        commit('SELECT_EXPERIMENT', experiment);
    },

    updateCurrentExperiment({ commit, getters }) {
        axios.get(`api/v1/experiments/${getters.currentExperiment.id}`).then(res => {
            commit('SELECT_EXPERIMENT', res.data.experiment)
        })
    },

    loadLastExperiment({ commit }) {
        axios.get('api/v1/experiments/lastexperiment', {
        }).then(res => {
            commit('SELECT_EXPERIMENT', res.data.experiment)
        })
    },

    exportCurrentExperiment({ commit, getters }) {
        if (getters.currentExperiment.id) {
            axios.get(`api/v1/experiments/export/${getters.currentExperiment.id}`).then(res => {
                commit('EXPORT_EXPERIMENT_FILE', res.data.file)
            })
        }
    },

    clearExperiments({ commit }) {
        commit('CLEAR_EXPERIMENTS')
    },

    clearCurrentExperiment({ commit }) {
        commit('CLEAR_CURRENT_EXPERIMENT')
    },

    filterExperiments({ commit }, filter) {
        commit('EXPERIMENTS_FILTER', filter)
    },

    queryExperiments({ commit }, params) {
        axios.post('api/v1/experiments/query', null, { params })
            .then(res => {
                commit('EXPERIMENTS_QUERY', res.data.results)
            })
    },

    deleteCurrentExperiment({ commit, getters }) {
        axios.delete(`api/v1/experiments/${getters.currentExperiment.id}`).then(
            (res) => {
                commit('UPDATE_MSG', res.data.msg)
            })
    },

    updateExperiment({ commit, getters }, experiment) {
        axios.put(`api/v1/experiments/${getters.currentExperiment.id}`, experiment).then(
            res => {
                commit('UPDATE_MSG', res.data.msg)
            }
        )
    },

    clearUpdateMsg({ commit }) {
        commit('UPDATE_MSG', null)
    },
}

const getters = {
    allExperiments(state) {
        return state.allExperiments ? state.allExperiments : null
    },

    currentExperiment(state) {
        return state.currentExperiment
    },

    importMsg(state) {
        return state.importMsg ? state.importMsg : null;
    },

    queriedExperiments(state) {
        return state.queriedExperiments

    },

    currentExperimentFile(state) {
        return state.currentExperimentFile
    },

    updateMsg(state) {
        return state.updateMsg
    },

    currentExperimentResults(state) {
        return state.currentExperimentResults ? state.currentExperimentResults : null
    },

    availableMarkers(state) {
        return state.availableMarkers ? state.availableMarkers.map(m => {
            return { value: m[0], text: m[1] };
          }) : null
    }
}

export default {
    state,
    mutations,
    actions,
    getters
}