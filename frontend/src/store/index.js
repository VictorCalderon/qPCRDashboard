import Vue from 'vue'
import Vuex from 'vuex'

// Add Vuex plugin
Vue.use(Vuex)

// Import Store Modules
import Projects from '@/store/modules/projects'
import Samples from '@/store/modules/samples'
import qPCRs from '@/store/modules/qpcrs'
import Settings from '@/store/modules/settings'
import Auth from '@/store/modules/auth'

// Export Modules
export default new Vuex.Store({
  modules: {
    Projects,
    Samples,
    qPCRs,
    Settings,
    Auth
  }
})