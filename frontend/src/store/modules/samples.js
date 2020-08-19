import axios from 'axios'
import Vue from 'vue'

const state = {
    currentSample: [],
    queriedSamples: [],
    sampleModifiedSignal: false,
}

const mutations = {

    'LOAD_SAMPLES'(state, allSamples) {
        Vue.set(state, 'allSamples', allSamples)
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

    'ADD_SAMPLE_RESULT'(state, result) {
        state.currentSample.result = result
    },

    'SAMPLES_FILTER'(state, sampleFilter) {
        Vue.set(state, 'filter', sampleFilter)
    },

    'TABLE_SAMPLE_FILTER'(state, sampleFilter) {
        Vue.set(state, 'sampleFilter', sampleFilter)
    },

    'TABLE_MARKER_FILTER'(state, markerFilter) {
        Vue.set(state, 'markerFilter', markerFilter)
    },

    'SAMPLE_MODIFIED'(state) {
        Vue.set(state, 'sampleModifiedSignal', !state.sampleModifiedSignal)
    },

    'SAMPLES_QUERY'(state, samples) {
        Vue.set(state, 'queriedSamples', samples)
    },
}

const actions = {
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

    filterSamples({ commit }, sampleFilter) {
        commit('SAMPLES_FILTER', sampleFilter)
    },

    modifySampleFilter({ commit }, sampleFilter) {
        commit('TABLE_SAMPLE_FILTER', sampleFilter);
    },

    modifyMarkerFilter({ commit }, markerFilter) {
        commit('TABLE_MARKER_FILTER', markerFilter);
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

    filteredTable(state) {

        // Filter samples
        const sTable = state.sampleFilter ? state.currentTable.filter(result => result.sample.includes(state.sampleFilter)) : state.currentTable;

        // Filter markers
        const mTable = state.markerFilter ? sTable.filter(result => result.marker == state.markerFilter) : sTable

        // Return table
        return mTable
    },

    queriedSamples(state) {
        return state.queriedSamples
    },

    currentTable(state) {
        return state.currentTable ? state.currentTable : []
    },
}


export default {
    state,
    mutations,
    actions,
    getters
}