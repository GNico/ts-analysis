import api from "../api/repository";
import { nanoid } from 'nanoid'


const defaultSettings = {
  name: '',
  description: '',
  client: '',
  data_options: [{
    contexts: [],
    tags: [],
    interval: '1h',
    start: null,
    end: null,
  }],
  model: [],
  saveId: undefined,
}

const state = {
  all: [],
  local: [],
  activeAnalysisId: '',
}

const getters = {
    getAnalysisById: (state) => (id) => {
        let item = state.local.find(elem => elem.id == id)
        return item ? item : {}
    },
    activeAnalysis: (state) => {
        let found = state.local.find(elem => elem.id == state.activeAnalysisId)
        return found ? found : {}
    },
}

const mutations = {
    set_all_analysis(state, payload) {
        state.all = payload
    },
    add_analysis(state, payload) {
        state.local.push(payload)
    },
    set_active(state, id) {
        state.activeAnalysisId = id
    },
    remove_analysis(state, id) {
        let index = state.local.findIndex(elem => elem.id == id)
        if (index > -1) {
            if (state.local[index].id == state.activeAnalysisId)
                state.activeAnalysisId = ''
            state.local.splice(index, 1)
        }
    },
    update_analysis(state, settings) {
        if (settings.hasOwnProperty('id')) {
            let index = state.local.findIndex(elem => elem.id == settings.id)
            if (index > -1) {
                let updated = { ...state.local[index] , ...settings}
                state.local.splice(index, 1, updated)
            }
        }
    }
}

const actions = {    
    fetchAllAnalysis(store) {
        return  api.getAllAnalysis()
                .then(response => {
                    store.commit('set_all_analysis', response.data)
                })
                .catch(error =>
                    console.log('error fetching analysis list'))
    },
    loadAnalysis(store, saveId) {
        return  api.getAnalysisDetails(saveId)
                .then(response => {
                    let settings = response.data
                    settings.id = nanoid(5)
                    store.commit('add_analysis', settings)
                    store.dispatch('setActiveAnalysis', settings.id)
                })
                .catch(error => console.log())
    }, 
    saveAnalysis({commit, getters, dispatch}, {id, name, description}) {
        const settings = getters.getAnalysisById(id)
        const objectToSave = { 
            client: settings.client,
            name: name,
            description: description,          
            data_options: settings.data_options,
            model: settings.model 
        }
        return  api.addNewAnalysis(objectToSave)
                .then(response => {
                    const saveId = response.data.id
                    commit('update_analysis', {id, name, description, saveId})
                    dispatch("fetchAllAnalysis")
                })
                .catch(error => console.log(error)) 
    },
    updateAnalysis({commit, getters, dispatch}, {id, name, description}) {
        const settings = getters.getAnalysisById(id)
        const objectToSave = { 
            client: settings.client,
            name: name,
            description: description,
            data_options: settings.data_options,           
            model: settings.model 
        }
        return  api.updateAnalysis(objectToSave, settings.saveId)
                .then(response => {
                    commit('update_analysis', {id, name, description})
                    dispatch("fetchAllAnalysis")
                })
                .catch(error => console.log(error))

    },
    deleteAnalysis({dispatch}, id) {
        return  api.deleteAnalysis(id)
                .then(response => dispatch("fetchAllAnalysis"))
                .catch(error => console.log(error))
    },
    deleteAnalysisList({dispatch}, idList) {
        console.log(idList)
        return  api.deleteAnalysisList(idList)
                .then(response => dispatch("fetchAllAnalysis"))
                .catch(error => console.log(error))
    }, 
    createLocalAnalysis(store) {
        const newId = nanoid(5)
        store.commit('add_analysis', { id: newId, ...defaultSettings })
        store.dispatch('setActiveAnalysis', newId)
    },
    closeLocalAnalysis(store, id) {
        store.commit('remove_analysis', id)
        store.dispatch('results/deleteResults', id,  {root: true}) 
    },
    updateLocalSettings(store, settings) {
        store.commit('update_analysis', settings)
    },
    setActiveAnalysis(store, id) {
        store.commit('set_active', id)
        store.commit('results/set_active_results', id, {root: true})
    },
    runAnalysis(store, analysisId) {
        let settings = store.getters.getAnalysisById(analysisId)
        store.dispatch("results/startAnalysis", settings, {root: true})
    }
}


export default {
    namespaced: true,
    getters,
    state,
    mutations,
    actions,
}