import Vue from 'vue'
import VueRouter from 'vue-router'

// Import views
// import Experiment from '../views/Experiment.vue'
import Experiment from '../views/Experiments2.vue'
import Dashboard from '../views/Dashboard.vue'
import Adjustments from '../views/Adjustments.vue'
// import Login from '../components/navigation/Login.vue'

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
    path: '/Dashboard',
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
  // {
  //   path: "/Login",
  //   name: 'Login',
  //   component: Login,
  // }
]

// Add routes
router.addRoutes(routes)


export default router