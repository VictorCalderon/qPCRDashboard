import axios from 'axios';
import Vue from 'vue';

const state = {
}

const mutations = {
  'STORE_USER'(state, { username }) {
    Vue.set(state, 'username', username)
  },

  'STORE_TOKEN'(state, { accessToken, refreshToken }) {
    Vue.set(state, 'accessToken', accessToken);
    Vue.set(state, 'refreshToken', refreshToken);
  },

  'STORE_ACCESS'(state, accessToken) {
    Vue.set(state, 'accessToken', accessToken);
  },

  'STORE_REFRESH'(state, refreshToken) {
    Vue.set(state, 'refreshToken', refreshToken);
  },

  'STORE_ERROR'(state, { errorMsg }) {
    Vue.set(state, 'errorMsg', errorMsg);
  },

  'CLEAR_TOKEN'(state) {
    Vue.set(state, 'accessToken', null);
    Vue.set(state, 'refreshToken', null)
  }
}

const actions = {
  authLogin({ commit }, { username, password }) {
    axios.post('auth/login', { username, password })
      .then(res => {

        // Store tokens
        commit('STORE_ACCESS', res.data.access_token);
        commit('STORE_REFRESH', res.data.refresh_token);

        // Store user data
        commit('STORE_USER', { username: username })
      })
      .catch(e => {
        commit('STORE_ERROR', { errorMsg: e.response.data.msg })
      })
  },

  authRefresh({ commit }) {
    // Get new token
    axios.post('auth/refresh')
      .then(res => {
        // Store access token
        commit('STORE_ACCESS', res.data.access_token)
      })

      .catch(e => {
        commit('STORE_ERROR', { errorMsg: e.response.data.msg })
      })
  },

  authSignUp({ commit }, { username, password, email }) {
    axios.post('users', { username, password, email })
      .then(res => {

        // Store tokens
        commit('STORE_ACCESS', res.data.access_token);
        commit('STORE_REFRESH', res.data.refresh_token);

        // Login new user
        commit('STORE_USER', { username: username })
        commit('STORE_ID', { userID: res.data.id })
      })

      .catch(e => {
        commit('STORE_ERROR', { errorMsg: e.response.data.msg })
      })
  },

  clearToken({ commit }) {
    commit('CLEAR_TOKEN')
  },

  authLogOut({ commit, dispatch }) {
    commit('CLEAR_TOKEN')
    dispatch('selectExperiment', null)
  }
}

const getters = {
  loginError(state) {
    return state.authErrorMsg
  },

  currentUser(state) {
    return state.username
  },

  accessToken(state) {
    return state.accessToken
  },

  needRefresh(state) {
    return state.needRefresh
  },

  refreshToken(state) {
    return state.refreshToken
  }
}

export default {
  state,
  mutations,
  actions,
  getters
}