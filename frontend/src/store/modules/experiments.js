import axios from 'axios'
import Vue from 'vue'

const state = {
    addExperimentsModal: false,
    searchExperimentsModal: false,
    currentExperimentFile: null,
    allExperiments: null,
    importMsg: null,
    recentExperiments: null,
    queriedExperiments: null,
    currentExperiment: null,
    currentExperimentResults: null
}

const mutations = {
    'LOAD_ALL_PROJECTS'(state, experiments) {
        Vue.set(state, 'allExperiments', experiments)
    },

    'TOGGLE_ADD_PROJECTS'(state) {
        Vue.set(state, 'addExperimentsModal', !state.addExperimentsModal)
    },

    'TOGGLE_SEARCH_PROJECTS'(state) {
        Vue.set(state, 'searchExperimentsModal', !state.searchExperimentsModal)
    },

    'POST_PROJECT_MSG'(state, errorMsg) {
        Vue.set(state, 'postExperimentMsg', errorMsg)
    },

    'LOAD_NEXT_PROJECTS'(state, nextUrl) {
        Vue.set(state, 'next', nextUrl)
    },

    'LOAD_PREV_PROJECTS'(state, prevUrl) {
        Vue.set(state, 'prev', prevUrl)
    },

    'SELECT_PROJECT'(state, experiment) {
        Vue.set(state, 'currentExperiment', experiment)
    },

    'IMPORT_MSG'(state, msg) {
        Vue.set(state, 'importMsg', msg)
    },

    'UPDATE_MSG'(state, msg) {
        Vue.set(state, 'updateMsg', msg)
    },

    'EXPORT_PROJECT_FILE'(state, file) {
        Vue.set(state, 'currentExperimentFile', file)
    },

    'CLEAR_PROJECTS'(state) {
        Vue.set(state, 'allExperiments', [])
    },

    'LOAD_RECENT_PROJECTS'(state) {
        if (state.recentExperiments == null && state.allExperiments != null) {
            const recentExperiments = state.allExperiments.slice(0, 6);
            Vue.set(state, 'recentExperiments', recentExperiments)
        }
        else return void 0

    },

    'ADD_RECENT_PROJECT'(state, experiment) {
        // Grab current data
        let recentExperiments = state.recentExperiments

        // Push new experiment
        recentExperiments.push(experiment)

        // Set as new data
        Vue.set(state, 'recentExperiments', recentExperiments)
    },

    'REMOVE_RECENT_PROJECT'(state, experiment) {
        // Grab current data
        let recentExperiments = state.recentExperiments

        // Find index
        let index = recentExperiments.findIndex(x => x.id === experiment.id);

        // Push new experiment
        recentExperiments.splice(index, 1)

        // Set as new data
        Vue.set(state, 'recentExperiments', recentExperiments)
    },

    'PROJECTS_QUERY'(state, experiments) {
        Vue.set(state, 'queriedExperiments', experiments)
    },

    'CLEAR_CURRENT_PROJECT'(state) {
        Vue.set(state, 'currentExperiment', null)
    },

    'SET_PROJECT_RESULTS'(state, results) {
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
                commit('LOAD_ALL_PROJECTS', res.data.results);
                commit('LOAD_NEXT_PROJECTS', res.data.next);
                commit('LOAD_PREV_PROJECTS', res.data.prev);
            }
        }).then(
            commit('LOAD_RECENT_PROJECTS')
        )
    },

    async getMarkers({ commit }) {
        await axios.get("api/v1/markers").then(res => {
            commit('AVAILABLE_MARKERS', res.data.marker);
        });
      },

    loadCurrentExperimentResults({ commit, getters }) {
        axios.get(`api/v1/experiments/${getters.currentExperiment.id}/results`).then(res => {
            commit('SET_PROJECT_RESULTS', res.data)
        })
    },

    toggleAddExperiments({ commit }) {
        commit('TOGGLE_ADD_PROJECTS')
    },

    toggleSearchExperiments({ commit }) {
        commit('TOGGLE_SEARCH_PROJECTS')
    },

    selectExperiment({ getters, commit }, experiment) {
        commit('SELECT_PROJECT', experiment);

        // Check if experiment is already added
        if (getters.recentExperiments) {

            // Search experiment in recent if we have it
            const search = getters.recentExperiments.filter(p => p.id == experiment.id)

            if (search.length == 0) {
                commit('ADD_RECENT_PROJECT', experiment);
            }
        }

    },

    loadSingleExperiment({ state, commit }, experiment) {
        // Grab current data
        let experiments = state.allExperiments

        // Push new experiment
        experiments.push(experiment)

        // Make this the new experiment
        commit('SET_AS_RECENT_PROJECTS', experiments)

    },

    selectCurrentExperiment({ commit, getters }) {
        if (getters.currentExperiment) {
            commit('SELECT_PROJECT', getters.currentExperiment.id)
        }
    },

    loadLastExperiment({ commit }) {
        axios.get('api/v1/experiments/lastexperiment', {
        }).then(res => {
            commit('SELECT_PROJECT', res.data.experiment)
        })
    },

    uploadExperiment({ commit }, formData) {
        axios.post('api/v1/experiments/import', formData, {
            headers: {
                "Content-Type": "multipart/form-data"
            }
        })

            .then(res => {
                commit('IMPORT_MSG', res.data.msg)
            })

            .catch(err => {
                commit('IMPORT_MSG', err.data.msg)
            })
    },

    exportCurrentExperiment({ commit, getters }) {
        if (getters.currentExperiment.id) {
            axios.get(`api/v1/experiments/export/${getters.currentExperiment.id}`).then(res => {
                commit('EXPORT_PROJECT_FILE', res.data.file)
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
        commit('CLEAR_PROJECTS')
    },

    clearCurrentExperiment({ commit }) {
        commit('CLEAR_CURRENT_PROJECT')
    },

    filterExperiments({ commit }, filter) {
        commit('PROJECTS_FILTER', filter)
    },

    queryExperiments({ commit }, params) {
        axios.post('api/v1/experiments/query', null, { params })
            .then(res => {
                commit('PROJECTS_QUERY', res.data.results)
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