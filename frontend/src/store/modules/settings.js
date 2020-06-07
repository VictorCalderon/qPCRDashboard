import Vue from 'vue'

const state = {
    export_sep: ',',
    exportName: 'resultados_covid.txt',
    labels: ['DETECTADO', 'NO DETECTADO', 'RETENIDO', 'INHIBIDO'],
    changeSettingsToggle: false,
    ampMin: 0,
    ampMax: 2
}

const mutations = {
    'TOGGLE_SETTINGS_MODAL'(state) {
        Vue.set(state, 'changeSettingsToggle', !state.changeSettingsToggle)
    },

    'MUTATE_SETTING'(state, payload) {
        Vue.set(state, payload.property, payload.with)
    },

    'MUTATE_LABELS'(state, newLabels) {
        Vue.set(state, 'labels', newLabels)
    },

    'CHANGE_EXPORT_NAME'(state, newExportName) {
        Vue.set(state, 'exportName', newExportName)
    },
}

const actions = {
    changeSetting({ commit }, setting, value) {
        commit('MUTATE_SETTING', { property: setting, with: value })
    },

    changeLabels({ commit }, newLabels) {
        commit('MUTATE_LABELS', newLabels)
    },

    toggleSettingsModal({ commit }) {
        commit('TOGGLE_SETTINGS_MODAL')
    },

    changeExportName({ commit }, newExportName) {
        commit('CHANGE_EXPORT_NAME', newExportName)
    },
}

const getters = {
    currentSettings(state) {
        return state
    },

    changeSettingsToggle(state) {
        return state.changeSettingsToggle
    },

    exportFilename(state) {
        return state.exportName
    },

    customExports(state) {
        const exportOptions = {
            'export_name': state.export_name,
            'export_sep': ','
        };
        return exportOptions
    },

    customLabels(state) {
        return state.labels
    },

    ampMin(state) {
        return state.ampMin
    },

    ampMax(state) {
        return state.ampMax
    }
}


export default {
    state,
    mutations,
    actions,
    getters
}