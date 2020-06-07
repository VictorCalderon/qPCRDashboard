// import axios from "axios"
import Vue from 'vue'

const state = {}

const mutations = {

    'LOAD_PROJECT_QPCR'(state, qPCRData) {
        Vue.set(state, 'ProjectqPCRs', qPCRData)
    },

}

const actions = {

    loadProjectqPCRs() {
        // console.log('Loading project');
        // axios.get(`api/v1/projects/${getters.currentProject.id}/qpcrs`).then(res => {
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

    projectqPCRs(state) {
        return state.ProjectqPCRs
    },

}

export default {
    state,
    mutations,
    actions,
    getters
}