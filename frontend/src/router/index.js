import Vue from 'vue'
import VueRouter from 'vue-router'

// Import views
import Experiment from '../views/Experiments.vue'
import Dashboard from '../views/Dashboard.vue'
import Adjustments from '../views/Adjustments.vue'

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
    path: '/Experiments',
    name: 'Experiments',
    component: Experiment,
  },
  {
    path: '/Adjustments',
    name: 'Adjustments',
    component: Adjustments,
  },
]

// Add routes
router.addRoutes(routes)


export default router