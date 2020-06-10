import axios from 'axios'
import Vue from 'vue'

const state = {
    addExperimentsModal: false,
    searchExperimentsModal: false,
    currentExperimentFile: null,
    allExperiments: null,
    importMsg: null,
    recentExperiments: null,
    queriedExperiments: [],
    currentExperiment: null,
    currentExperimentResults: null
}

const mutations = {
    'LOAD_ALL_EXPERIMENTS'(state, experiments) {
        Vue.set(state, 'allExperiments', experiments)
    },

    'TOGGLE_ADD_EXPERIMENTS'(state) {
        Vue.set(state, 'addExperimentsModal', !state.addExperimentsModal)
    },

    'TOGGLE_SEARCH_EXPERIMENTS'(state) {
        Vue.set(state, 'searchExperimentsModal', !state.searchExperimentsModal)
    },

    'POST_EXPERIMENT_MSG'(state, errorMsg) {
        Vue.set(state, 'postExperimentMsg', errorMsg)
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

    'IMPORT_MSG'(state, msg) {
        Vue.set(state, 'importMsg', msg)
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

    'LOAD_RECENT_EXPERIMENTS'(state) {
        if (state.recentExperiments == null && state.allExperiments != null) {
            const recentExperiments = state.allExperiments.slice(0, 6);
            Vue.set(state, 'recentExperiments', recentExperiments)
        }
        else return void 0

    },

    'ADD_RECENT_EXPERIMENT'(state, experiment) {
        // Grab current data
        let recentExperiments = state.recentExperiments

        // Push new experiment
        recentExperiments.push(experiment)

        // Set as new data
        Vue.set(state, 'recentExperiments', recentExperiments)
    },

    'REMOVE_RECENT_EXPERIMENT'(state, experiment) {
        // Grab current data
        let recentExperiments = state.recentExperiments

        // Find index
        let index = recentExperiments.findIndex(x => x.id === experiment.id);

        // Push new experiment
        recentExperiments.splice(index, 1)

        // Set as new data
        Vue.set(state, 'recentExperiments', recentExperiments)
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
    loadExperiments({ commit }) {
        axios.get('api/v1/experiments', {
        }).then(res => {
            if (res.data.results.length > 0) {
                commit('LOAD_ALL_EXPERIMENTS', res.data.results);
                commit('LOAD_NEXT_EXPERIMENTS', res.data.next);
                commit('LOAD_PREV_EXPERIMENTS', res.data.prev);
            }
        }).then(
            commit('LOAD_RECENT_EXPERIMENTS')
        )
    },

    async getMarkers({ commit }) {
        await axios.get("api/v1/markers").then(res => {
            commit('AVAILABLE_MARKERS', res.data.marker);
        });
    },

    loadCurrentExperimentResults({ commit, getters }) {
        axios.get(`api/v1/experiments/${getters.currentExperiment.id}/results`).then(res => {
            commit('SET_EXPERIMENT_RESULTS', res.data)
        })
    },

    toggleAddExperiments({ commit }) {
        commit('TOGGLE_ADD_EXPERIMENTS')
    },

    toggleSearchExperiments({ commit }) {
        commit('TOGGLE_SEARCH_EXPERIMENTS')
    },

    selectExperiment({ getters, commit }, experiment) {
        commit('SELECT_EXPERIMENT', experiment);

        // Check if experiment is already added
        if (getters.recentExperiments) {

            // Search experiment in recent if we have it
            const search = getters.recentExperiments.filter(p => p.id == experiment.id)

            if (search.length == 0) {
                commit('ADD_RECENT_EXPERIMENT', experiment);
            }
        }

    },

    loadSingleExperiment({ state, commit }, experiment) {
        // Grab current data
        let experiments = state.allExperiments

        // Push new experiment
        experiments.push(experiment)

        // Make this the new experiment
        commit('SET_AS_RECENT_EXPERIMENTS', experiments)

    },

    selectCurrentExperiment({ commit, getters }) {
        if (getters.currentExperiment) {
            commit('SELECT_EXPERIMENT', getters.currentExperiment.id)
        }
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

    deleteExperiment({ commit }, experiment_id) {
        axios.delete(`api/v1/experiments/${experiment_id}`, {
        }).then(res => {
            commit('EXPORT_MSG', res.data.msg)
        })
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

    clearImportMsg({ commit }) {
        commit('IMPORT_MSG', null)
    },
}

const getters = {
    allExperiments(state) {
        return state.allExperiments ? state.allExperiments : null
    },

    recentExperiments(state) {
        return state.recentExperiments ? state.recentExperiments.reverse().slice(0, 6) : null;
    },

    addExperimentsModal(state) {
        return state.addExperimentsModal
    },

    searchExperimentsModal(state) {
        return state.searchExperimentsModal
    },

    postExperimentError(state) {
        return state.postExperimentMsg
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
        return state.availableMarkers ? state.availableMarkers : null
    }
}

export default {
    state,
    mutations,
    actions,
    getters
}