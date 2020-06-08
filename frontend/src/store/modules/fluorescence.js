// import axios from "axios"
import Vue from 'vue'

const state = {}

const mutations = {

    'LOAD_PROJECT_QPCR'(state, FluorescenceData) {
        Vue.set(state, 'ExperimentFluorescences', FluorescenceData)
    },

}

const actions = {

    loadExperimentFluorescences() {
        // console.log('Loading experiment');
        // axios.get(`api/v1/experiments/${getters.currentExperiment.id}/qpcrs`).then(res => {
        //     const qpcrs = res.data.qpcrs.map(qpcr => {
        //         const qpcrSample = getters.currentSamples.find(sample => sample.id == qpcr.id);
        //         return {
        //             serialized_rn: [...qpcr.serialized_rn.split(',')],
        //             id: qpcr.id,
        //             label: qpcr.marker,
        //             sample: qpcrSample.id
        //         }
        //     });
        //     console.log(qpcrs);
        //     commit('LOAD_PROJECT_QPCR', qpcrs)
        // })
    },

}

const getters = {

    experimentFluorescences(state) {
        return state.ExperimentFluorescences
    },

}

export default {
    state,
    mutations,
    actions,
    getters
}