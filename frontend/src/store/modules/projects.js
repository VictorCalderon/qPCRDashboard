import axios from 'axios'
import Vue from 'vue'

const state = {
    addProjectsModal: false,
    searchProjectsModal: false,
    currentProjectFile: null,
    allProjects: null,
    importMsg: null,
    recentProjects: null,
    queriedProjects: null,
    currentProject: null,
    currentProjectResults: null
}

const mutations = {
    'LOAD_ALL_PROJECTS'(state, projects) {
        Vue.set(state, 'allProjects', projects)
    },

    'TOGGLE_ADD_PROJECTS'(state) {
        Vue.set(state, 'addProjectsModal', !state.addProjectsModal)
    },

    'TOGGLE_SEARCH_PROJECTS'(state) {
        Vue.set(state, 'searchProjectsModal', !state.searchProjectsModal)
    },

    'POST_PROJECT_MSG'(state, errorMsg) {
        Vue.set(state, 'postProjectMsg', errorMsg)
    },

    'LOAD_NEXT_PROJECTS'(state, nextUrl) {
        Vue.set(state, 'next', nextUrl)
    },

    'LOAD_PREV_PROJECTS'(state, prevUrl) {
        Vue.set(state, 'prev', prevUrl)
    },

    'SELECT_PROJECT'(state, project) {
        Vue.set(state, 'currentProject', project)
    },

    'IMPORT_MSG'(state, msg) {
        Vue.set(state, 'importMsg', msg)
    },

    'UPDATE_MSG'(state, msg) {
        Vue.set(state, 'updateMsg', msg)
    },

    'EXPORT_PROJECT_FILE'(state, file) {
        Vue.set(state, 'currentProjectFile', file)
    },

    'CLEAR_PROJECTS'(state) {
        Vue.set(state, 'allProjects', [])
    },

    'LOAD_RECENT_PROJECTS'(state) {
        if (state.recentProjects == null && state.allProjects != null) {
            const recentProjects = state.allProjects.slice(0, 6);
            Vue.set(state, 'recentProjects', recentProjects)
        }
        else return void 0

    },

    'ADD_RECENT_PROJECT'(state, project) {
        // Grab current data
        let recentProjects = state.recentProjects

        // Push new project
        recentProjects.push(project)

        // Set as new data
        Vue.set(state, 'recentProjects', recentProjects)
    },

    'REMOVE_RECENT_PROJECT'(state, project) {
        // Grab current data
        let recentProjects = state.recentProjects

        // Find index
        let index = recentProjects.findIndex(x => x.id === project.id);

        // Push new project
        recentProjects.splice(index, 1)

        // Set as new data
        Vue.set(state, 'recentProjects', recentProjects)
    },

    'PROJECTS_QUERY'(state, projects) {
        Vue.set(state, 'queriedProjects', projects)
    },

    'CLEAR_CURRENT_PROJECT'(state) {
        Vue.set(state, 'currentProject', null)
    },

    'SET_PROJECT_RESULTS'(state, results) {
        Vue.set(state, 'currentProjectResults', results)
    }
}

const actions = {
    loadProjects({ commit }) {
        axios.get('api/v1/projects', {
        }).then(res => {
            if (res.data.results.length > 0) {
                commit('LOAD_ALL_PROJECTS', res.data.results);
                commit('LOAD_NEXT_PROJECTS', res.data.next);
                commit('LOAD_PREV_PROJECTS', res.data.prev);
            }
        }).then(
            commit('LOAD_RECENT_PROJECTS')
        )


    },

    loadCurrentProjectResults({ commit, getters }) {
        axios.get(`api/v1/projects/${getters.currentProject.id}/results`).then(res => {
            commit('SET_PROJECT_RESULTS', res.data)
        }
        )
    },

    toggleAddProjects({ commit }) {
        commit('TOGGLE_ADD_PROJECTS')
    },

    toggleSearchProjects({ commit }) {
        commit('TOGGLE_SEARCH_PROJECTS')
    },

    selectProject({ getters, commit }, project) {
        commit('SELECT_PROJECT', project);

        // Check if project is already added
        if (getters.recentProjects) {

            // Search project in recent if we have it
            const search = getters.recentProjects.filter(p => p.id == project.id)

            if (search.length == 0) {
                commit('ADD_RECENT_PROJECT', project);
            }
        }

    },

    loadSingleProject({ state, commit }, project) {
        // Grab current data
        let projects = state.allProjects

        // Push new project
        projects.push(project)

        // Make this the new project
        commit('SET_AS_RECENT_PROJECTS', projects)

    },

    selectCurrentProject({ commit, getters }) {
        if (getters.currentProject) {
            commit('SELECT_PROJECT', getters.currentProject.id)
        }
    },

    loadLastProject({ commit }) {
        axios.get('api/v1/projects/lastproject', {
        }).then(res => {
            commit('SELECT_PROJECT', res.data.project)
        })
    },

    uploadExperiment({ commit }, formData) {
        axios.post('api/v1/projects/import', formData, {
            headers: {
                "Content-Type": "multipart/form-data"
            }
        })

            .then(res => {
                commit('IMPORT_MSG', res.data.msg)
            })

            .catch(err => {
                commit('IMPORT_MSG', err.data.msg)
            })
    },

    exportCurrentProject({ commit, getters }) {
        if (getters.currentProject.id) {
            axios.get(`api/v1/projects/export/${getters.currentProject.id}`).then(res => {
                commit('EXPORT_PROJECT_FILE', res.data.file)
            })
        }
    },

    deleteProject({ commit }, project_id) {
        axios.delete(`api/v1/projects/${project_id}`, {
        }).then(res => {
            commit('EXPORT_MSG', res.data.msg)
        })
    },

    clearProjects({ commit }) {
        commit('CLEAR_PROJECTS')
    },

    clearCurrentProject({ commit }) {
        commit('CLEAR_CURRENT_PROJECT')
    },

    filterProjects({ commit }, filter) {
        commit('PROJECTS_FILTER', filter)
    },

    queryProjects({ commit }, params) {
        axios.post('api/v1/projects/query', null, { params })
            .then(res => {
                commit('PROJECTS_QUERY', res.data.results)
            })
    },

    deleteCurrentProject({ commit, getters }) {
        axios.delete(`api/v1/projects/${getters.currentProject.id}`).then(
            (res) => {
                commit('UPDATE_MSG', res.data.msg)
            })
    },

    updateProject({ commit, getters }, project) {
        axios.put(`api/v1/projects/${getters.currentProject.id}`, project).then(
            res => {
                commit('UPDATE_MSG', res.data.msg)
            }
        )
    },

    clearUpdateMsg({ commit }) {
        commit('UPDATE_MSG', null)
    },

    clearImportMsg({ commit }) {
        commit('IMPORT_MSG', null)
    },
}

const getters = {
    allProjects(state) {
        return state.allProjects ? state.allProjects : null
    },

    recentProjects(state) {
        return state.recentProjects ? state.recentProjects.reverse().slice(0, 6) : null;
    },

    addProjectsModal(state) {
        return state.addProjectsModal
    },

    searchProjectsModal(state) {
        return state.searchProjectsModal
    },

    postProjectError(state) {
        return state.postProjectMsg
    },

    currentProject(state) {
        return state.currentProject
    },

    importMsg(state) {
        return state.importMsg ? state.importMsg : null;
    },

    queriedProjects(state) {
        return state.queriedProjects

    },

    currentProjectFile(state) {
        return state.currentProjectFile
    },

    updateMsg(state) {
        return state.updateMsg
    },

    currentProjectResults(state) {
        return state.currentProjectResults ? state.currentProjectResults : null
    }
}

export default {
    state,
    mutations,
    actions,
    getters
}