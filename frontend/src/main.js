import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

// import { Promise } from 'es6-promise'

// Import BootstrapVue
import { BootstrapVue } from 'bootstrap-vue'

// Import CSS
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

// Install BootstrapVue
Vue.use(BootstrapVue)

// Add HTTP functionality
import axios from 'axios'

// Set basic URL
axios.defaults.baseURL = 'http://localhost:5000/'

// Set token interceptor
axios.interceptors.request.use(config => {
  const access_token = store.getters.accessToken;

  if (config.url == 'auth/refresh') {

    // Get refresh token
    const refresh_token = store.getters.refreshToken;

    // Add Authorization header
    config.headers['Authorization'] = `Bearer ${refresh_token}`

    // Return configuration
    return config
  }

  if (access_token) {
    config.headers['Authorization'] = `Bearer ${access_token}`
  }

  return config
})

// Response interceptor
axios.interceptors.response.use(res => {
  return res;
},

  async (error) => {
    if (error) {
      if (error.response.status !== 401) {
        return new Promise((resolve, reject) => {
          reject(error)
        })
      }

      if (error.config.url == 'api/v1/auth/refresh' && error.response.msg == 'Token is Invalid') {
        store.dispatch('ClearToken');
      }

      return store.dispatch('authRefresh')
        .then(
          () => {
            return new Promise((resolve) => {

              // Get error config
              let config = error.config;

              // Add authorization header to new request
              config.headers['Authorization'] = `Bearer ${store.getters.accessToken}`

              // Launch raw request
              axios.request(config).then(
                res => {
                  resolve(res);
                }
              ).catch((error) => {
                Promise.reject(error);
              })
            })
          }
        )
    }
  })

// Add DateTime Filter
import moment from 'moment'

Vue.filter('formatDate', function (value) {
  if (value) {
    moment.locale("en");
    let date = moment.utc(String(value));
    return date.format("ll");
  }
})

Vue.filter('shortName', function (value) {
  if (value) {
    return value.slice(0, 20)
  }
})

Vue.config.productionTip = false


new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
