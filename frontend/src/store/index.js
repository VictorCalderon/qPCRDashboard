import Vue from 'vue'
import Vuex from 'vuex'

// Add Vuex plugin
Vue.use(Vuex)

// Import Store Modules
import Experiments from '@/store/modules/experiments'
import Samples from '@/store/modules/samples'
import Auth from '@/store/modules/auth'
import Dashboard from '@/store/modules/dashboard'
import Adjustments from '@/store/modules/adjustments'


// Export Modules
export default new Vuex.Store({
  modules: {
    Experiments,
    Samples,
    Auth,
    Dashboard,
    Adjustments
  }
})