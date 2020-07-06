import axios from 'axios'
import Vue from 'vue'

const state = {
    mapCenter: [19.007237, -70.41502],
    samplingSites: [],
    briefingData: { 'samples': 56812, 'experiments': 1232 },
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
    }
}

const actions = {
    updateBriefingData({ commit }, mode) {
        axios.get(`api/v1/dashboard/briefing/${mode}`).then(
            res => {
                commit('SET_BRIEFING_DATA', res.data)
            }
        )
    },

    updateMapCenter({ commit }, newCenter) {
        commit('SET_MAP_CENTER', newCenter)
    },

    updateSamplingSites({ commit }) {

        // Dummy data
        const latlngData = [
            {
                loc: [18.4358, -69.9853],
                name: "Sede Central",
                totalSamples: 19800
            },
            {
                loc: [19.4548, -70.6929],
                name: "Santiago",
                totalSamples: 12800
            },
            {
                loc: [19.22064, -70.5632],
                name: "La Vega",
                totalSamples: 11000
            }
        ];

        // Commit data
        commit('SET_SAMPLING_SITE_COORDINATES', latlngData)
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
    }
}


export default {
    state,
    mutations,
    actions,
    getters
}