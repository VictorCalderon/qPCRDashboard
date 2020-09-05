import Vue from 'vue'
import Vuex from 'vuex'

// Add Vuex plugin
Vue.use(Vuex)

// Import Store Modules
import Analysis from '@/store/modules/analysis'
import Samples from '@/store/modules/samples'
import Patients from '@/store/modules/patients'
import Auth from '@/store/modules/auth'
import Dashboard from '@/store/modules/dashboard'
import Adjustments from '@/store/modules/adjustments'
import Experiment from '@/store/modules/experiment'
// import PlateSetup from '@/store/modules/platesetup'


// Export Modules
export default new Vuex.Store({
  modules: {
    Analysis,
    Samples,
    Patients,
    Auth,
    Dashboard,
    Adjustments,
    Experiment,
    // PlateSetup
  }
})