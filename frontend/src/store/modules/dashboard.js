import axios from 'axios'
import Vue from 'vue'

const state = {
    mapCenter: [19.007237, -70.41502],
    samplingSites: [],
    briefingData: {},
    ampPercData: null,
    tagDistribution: null
}

const mutations = {
    SET_MAP_CENTER(state, newCenter) {
        Vue.set(state, 'mapCenter', newCenter);
    },

    SET_SAMPLING_SITE_COORDINATES(state, samplingSites) {
        Vue.set(state, 'samplingSites', samplingSites)
    },

    SET_BRIEFING_DATA(state, briefingData) {
        Vue.set(state, 'briefingData', briefingData)
    },

    SET_AMP_PERC(state, ampPercData) {
        Vue.set(state, 'ampPercData', ampPercData)
    },

    SET_TAG_DISTRIBUTION(state, tagDistribution) {
        Vue.set(state, 'tagDistribution', tagDistribution)
    }
}

const actions = {

    updateTagDistribution({ commit }) {
        axios.get('api/v1/dashboard/tagdistrib').then(
            res => {
                commit('SET_TAG_DISTRIBUTION', res.data)
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

    ampStatusTimeline({ commit }) {
        axios.get('api/v1/dashboard/ampstatdata').then(
            res => {
                commit('SET_AMP_PERC', res.data)
            }
        )
    },

    updateMapCenter({ commit }, newCenter) {
        commit('SET_MAP_CENTER', newCenter)
    },

    updateSamplingSites({ commit }) {
        axios.get('api/v1/dashboard/locatedsamples').then(
            res => {
                commit('SET_SAMPLING_SITE_COORDINATES', res.data)
            }
        )

    }
}


const getters = {
    mapCenter(state) {
        return state.mapCenter
    },

    samplingSites(state) {
        return state.samplingSites
    },

    briefingData(state) {
        return state.briefingData
    },

    ampPercData() {
        return state.ampPercData
    },

    tagDistribution() {
        return state.tagDistribution
    }
}


export default {
    state,
    mutations,
    actions,
    getters
}