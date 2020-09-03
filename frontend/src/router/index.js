import Vue from 'vue'
import VueRouter from 'vue-router'

// Import views
import Analysis from '../views/Analysis.vue'
import Dashboard from '../views/Dashboard.vue'
import Adjustments from '../views/Adjustments.vue'
import Experiment from '../views/Experiment.vue'

// User plugin
Vue.use(VueRouter)

// Configure router
const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
})

// Configure routes
const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard,
  },
  {
    path: '/Analysis',
    name: 'Analysis',
    component: Analysis,
  },
  {
    path: '/Adjustments',
    name: 'Adjustments',
    component: Adjustments,
  },
  {
    path: '/Experiment',
    name: 'Experiment',
    component: Experiment
  }
]

// Add routes
router.addRoutes(routes)


export default router