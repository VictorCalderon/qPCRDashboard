import axios from 'axios'
import Vue from 'vue'

const state = {
    sampleModifiedSignal: false,
    currentSample: [],
    queriedSamples: [],
    sampleLocationSchemas: null,
}

const mutations = {

    'LOAD_SAMPLES'(state, allSamples) {
        Vue.set(state, 'allSamples', allSamples)
    },

    'UPDATE_SAMPLE_LOCATION_SCHEMAS'(state, allSchemas) {
        Vue.set(state, 'sampleLocationSchemas', allSchemas)
    },

    'LOAD_NEXT_SAMPLES'(state, nextUrl) {
        Vue.set(state, 'next', nextUrl)
    },

    'LOAD_PREV_SAMPLES'(state, prevUrl) {
        Vue.set(state, 'prev', prevUrl)
    },

    'LOAD_CURRENT_SAMPLES'(state, currentSamples) {
        Vue.set(state, 'currentSamples', currentSamples);
    },

    'LOAD_CURRENT_TABLE'(state, currentTable) {
        Vue.set(state, 'currentTable', currentTable);
    },

    'SELECT_SAMPLE'(state, sample) {
        Vue.set(state, 'currentSample', sample)
    },

    'LOAD_SAMPLE_Fluorescences'(state, fluorescences) {
        Vue.set(state, 'currentSampleFluorescences', fluorescences)
    },

    'ADD_SAMPLE_RESULT'(state, result) {
        state.currentSample.result = result
    },

    'SAMPLES_FILTER'(state, filter) {
        Vue.set(state, 'filter', filter)
    },

    'TABLE_FILTER'(state, filter) {
        Vue.set(state, 'filter', filter)
    },

    'SAMPLE_MODIFIED'(state) {
        Vue.set(state, 'sampleModifiedSignal', !state.sampleModifiedSignal)
    },

    'SAMPLES_QUERY'(state, samples) {
        Vue.set(state, 'queriedSamples', samples)
    },
}

const actions = {

    getSampleLocationSchemas({ commit }) {
        axios.get('api/v1/dashboard/samplelocation').then(res => {
            commit('UPDATE_SAMPLE_LOCATION_SCHEMAS', res.data)
        })
    },

    updateSampleLocationSchemas({ commit }, schema) {
        axios.post('api/v1/dashboard/samplelocation', schema).then(() => {
            commit('SAMPLE_MODIFIED');
        })
    },

    deleteSampleLocationSchema({ commit }, schema_id) {
        axios.delete(`api/v1/dashboard/samplelocation/${schema_id}`).then(() => {
            commit('SAMPLE_MODIFIED');
        })
    },

    loadSamples({ commit }) {
        axios.get('api/v1/samples', {
        }).then(res => {
            commit('LOAD_SAMPLES', res.data.results);
            commit('LOAD_NEXT_SAMPLES', res.data.next);
            commit('LOAD_PREV_SAMPLES', res.data.prev)
        })
    },

    selectSample({ commit }, sample) {
        commit('SELECT_SAMPLE', sample);
    },

    loadCurrentSamples({ getters, commit }) {
        if (!getters.currentExperiment) return void 0;
        axios.get(`api/v1/experiments/${getters.currentExperiment.id}/samples`, {
        }).then(
            res => {
                commit('LOAD_CURRENT_SAMPLES', res.data.samples)
            }
        );
    },

    loadCurrentTable({ getters, commit }) {
        if (!getters.currentExperiment) return void 0;
        axios.get(`api/v1/experiments/${getters.currentExperiment.id}/table`, {
        }).then(
            res => {
                commit('LOAD_CURRENT_TABLE', res.data.samples)
            }
        );
    },

    updateSample({ commit, getters }, result) {
        commit('ADD_SAMPLE_RESULT', result);
        commit('SAMPLE_MODIFIED');

        axios.put(`api/v1/samples/${getters.currentSample.id}`, getters.currentSample, {
        }).then(res => { return res.msg })
    },

    filterSamples({ commit }, filter) {
        commit('SAMPLES_FILTER', filter)
    },

    filterTable({ commit }, filter) {
        commit('TABLE_FILTER', filter)
    },

    querySamples({ commit }, params) {
        axios.post('api/v1/samples/query', null, { params })
            .then(res => {
                commit('SAMPLES_QUERY', res.data)
            })
    },
}


const getters = {
    allSamples(state) {
        return state.allSamples
    },

    sampleLocationSchemas(state) {
        return state.sampleLocationSchemas
    },

    currentSamples(state) {
        return state.currentSamples
            ? state.currentSamples
            : [];
    },

    currentSample(state) {
        return state.currentSample;
    },

    currentSampleFluorescences(state) {
        return state.currentSampleFluorescences ? state.currentSampleFluorescences : [];
    },

    modificationSignal(state) {
        return state.sampleModifiedSignal
    },

    filteredSamples(state) {
        return state.filter
            ? state.currentSamples.filter(sample => sample.sample.includes(state.filter))
            : state.currentSamples;
    },

    filteredTable(state) {
        return state.filter
            ? state.currentTable.filter(result => result.sample.includes(state.filter))
            : state.currentTable;
    },

    queriedSamples(state) {
        return state.queriedSamples
    },

    currentTable(state) {
        return state.currentTable ? state.currentTable : null
    }
}


export default {
    state,
    mutations,
    actions,
    getters
}