import axios from 'axios'
import Vue from 'vue'

const state = {
    targetGroups: [],
    sampleLocationSchemas: null,
    mapCenter: [19.007237, -70.41502],
    markerSize: 50,
    markerOpacity: 0.8,
    markerSizeOpacity: [50, 0.8],
    groupModified: false,
    availableMarkers: []
}

const mutations = {
    SET_TARGET_GROUPS(state, targetGroups) {
        Vue.set(state, 'targetGroups', targetGroups)
    },

    SET_MAP_MARKER_SIZE(state, markerSize) {
        // Save to local storage
        localStorage.setItem('markerSize', markerSize);

        // Save to Vue
        Vue.set(state, 'markerSize', markerSize);
    },

    SET_MAP_MARKER_OPACITY(state, markerOpacity) {
        // Save to local storage
        localStorage.setItem('markerOpacity', markerOpacity);

        // Save to Vue
        Vue.set(state, 'markerOpacity', markerOpacity);
    },

    SET_MAP_CENTER(state, newCenter) {
        // Save to local storage
        localStorage.setItem('newCenter', newCenter);

        // Save to Vue
        Vue.set(state, 'mapCenter', newCenter);
    },

    UPDATE_SAMPLE_LOCATION_SCHEMAS(state, allSchemas) {
        Vue.set(state, 'sampleLocationSchemas', allSchemas)
    },

    GROUP_MODIFIED(state) {
        Vue.set(state, 'groupModified', !state.groupModified)
    },

    SET_AVAILABLE_MARKERS(state, markers) {
        Vue.set(state, 'availableMarkers', markers)
    }
}

const actions = {
    getAvailableMarkers({ commit }) {
        axios.get('api/v1/adjustments/markers')
            .then(res => {
                commit('SET_AVAILABLE_MARKERS', JSON.parse(res.data))
            })
    },

    modifyAvailableMarkers({ commit }, markers) {
        axios.post('api/v1/adjustments/markers', { 'markers': markers })
            .then(res => { commit('SET_AVAILABLE_MARKERS', res.data.markers) })
    },


    getTargetGroups({ commit }) {
        axios.get('api/v1/adjustments/targetgroups')
            .then(res => { commit('SET_TARGET_GROUPS', res.data) })
    },

    updateTargetGroups({ commit }, group) {
        axios.post('api/v1/adjustments/targetgroups', group).then(() => {
            commit('GROUP_MODIFIED')
        })
    },

    deleteTargetGroup({ commit }, group) {
        axios.delete(`api/v1/adjustments/targetgroups/${group.id}`).then(() => {
            commit('GROUP_MODIFIED')
        })
    },

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

    updateMapCenter({ commit }, newCenter) {
        commit('SET_MAP_CENTER', newCenter)
    },

    updateMarkerSize({ commit }, markerSize) {
        commit('SET_MAP_MARKER_SIZE', markerSize)
    },

    updateMarkerOpacity({ commit }, markerOpacity) {
        commit('SET_MAP_MARKER_OPACITY', markerOpacity)
    },
}


const getters = {
    targetGroups(state) {
        return state.targetGroups
    },

    availableMarkers(state) {
        return state.availableMarkers
    },

    mapCenter(state) {

        // Check if saved in LocalStorage
        const mapCenter = localStorage.getItem('mapCenter') || null;

        if (mapCenter) {
            return mapCenter
        }

        return state.mapCenter
    },

    markerSize(state) {

        // Check if saved in LocalStorage
        const markerSize = localStorage.getItem('markerSize') || null;

        if (markerSize) {
            return markerSize
        }

        return state.markerSize
    },

    markerOpacity(state) {

        // Check if saved in LocalStorage
        const markerOpacity = localStorage.getItem('markerOpacity') || null;

        if (markerOpacity) {
            return markerOpacity
        }
        return state.markerOpacity
    },

    sampleLocationSchemas(state) {
        return state.sampleLocationSchemas
    },

}


export default {
    state,
    mutations,
    actions,
    getters
}