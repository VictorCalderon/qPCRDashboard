import Vue from 'vue'
import Vuex from 'vuex'

// Add Vuex plugin
Vue.use(Vuex)

// Import Store Modules
import Experiments from '@/store/modules/experiments'
import Samples from '@/store/modules/samples'
import Fluorescences from '@/store/modules/fluorescence'
import Settings from '@/store/modules/settings'
import Auth from '@/store/modules/auth'

// Export Modules
export default new Vuex.Store({
  modules: {
    Experiments,
    Samples,
    Fluorescences,
    Settings,
    Auth
  }
})