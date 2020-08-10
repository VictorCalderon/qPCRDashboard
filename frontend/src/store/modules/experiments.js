import axios from 'axios'
import Vue from 'vue'

const state = {
    sampleList: [
        {
            id: 0,
            well: "A1",
            sample: "2001231232M1",
            marker: "RNase P",
            amp: true,
            cq: 28,
            score: 0.8
        },
        {
            id: 1,
            well: "A1",
            sample: "2001231232M1",
            marker: "ORF1ab",
            amp: false,
            cq: 0,
            score: 0.1
        },
        {
            id: 2,
            well: "A1",
            sample: "2001231232M1",
            marker: "N Gene",
            amp: true,
            cq: 30,
            score: 0.7
        },
        {
            id: 3,
            well: "A1",
            sample: "2001231232M1",
            marker: "S Gene",
            amp: true,
            cq: 27,
            score: 0.7
        },
        {
            id: 0,
            well: "A1",
            sample: "2001231232M1",
            marker: "RNase P",
            amp: true,
            cq: 28,
            score: 0.8
        },
        {
            id: 1,
            well: "A1",
            sample: "2001231232M1",
            marker: "ORF1ab",
            amp: false,
            cq: 0,
            score: 0.1
        },
        {
            id: 2,
            well: "A1",
            sample: "2001231232M1",
            marker: "N Gene",
            amp: true,
            cq: 30,
            score: 0.7
        },
        {
            id: 3,
            well: "A1",
            sample: "2001231232M1",
            marker: "S Gene",
            amp: true,
            cq: 27,
            score: 0.7
        },
        {
            id: 0,
            well: "A1",
            sample: "2001231232M1",
            marker: "RNase P",
            amp: true,
            cq: 28,
            score: 0.8
        },
        {
            id: 1,
            well: "A1",
            sample: "2001231232M1",
            marker: "ORF1ab",
            amp: false,
            cq: 0,
            score: 0.1
        },
        {
            id: 2,
            well: "A1",
            sample: "2001231232M1",
            marker: "N Gene",
            amp: true,
            cq: 30,
            score: 0.7
        },
        {
            id: 3,
            well: "A1",
            sample: "2001231232M1",
            marker: "S Gene",
            amp: true,
            cq: 27,
            score: 0.7
        },
        {
            id: 0,
            well: "A1",
            sample: "2001231232M1",
            marker: "RNase P",
            amp: true,
            cq: 28,
            score: 0.8
        },
        {
            id: 1,
            well: "A1",
            sample: "2001231232M1",
            marker: "ORF1ab",
            amp: false,
            cq: 0,
            score: 0.1
        },
        {
            id: 2,
            well: "A1",
            sample: "2001231232M1",
            marker: "N Gene",
            amp: true,
            cq: 30,
            score: 0.7
        },
        {
            id: 3,
            well: "A1",
            sample: "2001231232M1",
            marker: "S Gene",
            amp: true,
            cq: 27,
            score: 0.7
        },
        {
            id: 0,
            well: "A1",
            sample: "2001231232M1",
            marker: "RNase P",
            amp: true,
            cq: 28,
            score: 0.8
        },
        {
            id: 1,
            well: "A1",
            sample: "2001231232M1",
            marker: "ORF1ab",
            amp: false,
            cq: 0,
            score: 0.1
        },
        {
            id: 2,
            well: "A1",
            sample: "2001231232M1",
            marker: "N Gene",
            amp: true,
            cq: 30,
            score: 0.7
        },
        {
            id: 3,
            well: "A1",
            sample: "2001231232M1",
            marker: "S Gene",
            amp: true,
            cq: 27,
            score: 0.7
        },
        {
            id: 0,
            well: "A1",
            sample: "2001231232M1",
            marker: "RNase P",
            amp: true,
            cq: 28,
            score: 0.8
        },
        {
            id: 1,
            well: "A1",
            sample: "2001231232M1",
            marker: "ORF1ab",
            amp: false,
            cq: 0,
            score: 0.1
        },
        {
            id: 2,
            well: "A1",
            sample: "2001231232M1",
            marker: "N Gene",
            amp: true,
            cq: 30,
            score: 0.7
        },
        {
            id: 3,
            well: "A1",
            sample: "2001231232M1",
            marker: "S Gene",
            amp: true,
            cq: 27,
            score: 0.7
        },

    ],

    LSCData: [
        {
            label: "2001232123M1",
            x: 0.2, y: 0.7,
            cluster: 0
        },
        {
            label: "2001232123M1",
            x: 0.4, y: 0.6,
            cluster: 0
        },
        {
            label: "2001232123M1",
            x: 0.3, y: 0.7,
            cluster: 0
        },
        {
            label: "2001232123M1",
            x: 0.4, y: 0.8,
            cluster: 0
        },
        {
            label: "2001232123M1",
            x: 4, y: 2,
            cluster: 1
        },
        {
            label: "2001232123M1",
            x: 4.2, y: 2.5,
            cluster: 1
        },
        {
            label: "2001232123M1",
            x: 4.7, y: 2.2,
            cluster: 1
        },
        {
            label: "2001232123M1",
            x: 3.8, y: 2.7,
            cluster: 1
        },
        {
            label: "2001232123M1",
            x: 4.1, y: 2.6,
            cluster: 1
        },
        {
            label: "2001232121M1",
            x: 1.1, y: 2.1,
            cluster: 2
        },
        {
            label: "2001232121M1",
            x: 1.3, y: 2.2,
            cluster: 2
        },
        {
            label: "2001232121M1",
            x: 1.2, y: 2.3,
            cluster: 2
        },
        {
            label: "2001232121M1",
            x: 1.1, y: 1.9,
            cluster: 2
        },
        {
            label: "2001232121M1",
            x: 1, y: 2.4,
            cluster: 2
        }
    ],


}

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

    'SET_EXPERIMENT_FLUORESCENCES'(state, results) {
        Vue.set(state, 'currentExperimentFluorescences', results)
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

    loadCurrentExperimentFluorescences({ commit, getters }) {
        axios.get(`api/v1/experiments/${getters.currentExperiment.id}/fluorescences`).then(res => {
            commit('SET_EXPERIMENT_FLUORESCENCES', res.data.fluorescence_data)
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

    currentExperimentFluorescences(state) {
        return state.currentExperimentFluorescences
    },

    availableMarkers(state) {
        return state.availableMarkers ? state.availableMarkers.map(m => {
            return { value: m[0], text: m[1] };
        }) : null
    },

    LSCData(state) {
        return state.LSCData
    },

}

export default {
    state,
    mutations,
    actions,
    getters
}