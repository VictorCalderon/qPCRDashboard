import axios from 'axios'
import Vue from 'vue'

const state = {
    sampleModifiedSignal: false,
    currentSample: [],
    queriedSamples: [],
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

    selectSample({ state, commit }, sample_id) {
        const sample = state.currentSamples.find(s => s.id == sample_id);
        commit('SELECT_SAMPLE', sample);

        axios.get(`api/v1/samples/${sample_id}/fluorescences`, {
        }).then(
            res => { commit('LOAD_SAMPLE_Fluorescences', res.data.fluorescence_data) }
        )
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

    updateSample({ commit, getters }, result) {
        commit('ADD_SAMPLE_RESULT', result);
        commit('SAMPLE_MODIFIED');

        axios.put(`api/v1/samples/${getters.currentSample.id}`, getters.currentSample, {
        }).then(res => { return res.msg })
    },

    filterSamples({ commit }, filter) {
        commit('SAMPLES_FILTER', filter)
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

    filteredSamples(state) {
        return state.filter
            ? state.currentSamples.filter(sample => sample.sample.includes(state.filter))
            : state.currentSamples;
    },

    queriedSamples(state) {
        return state.queriedSamples
    }
}


export default {
    state,
    mutations,
    actions,
    getters
}