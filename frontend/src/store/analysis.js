import api from "../api/repository";
import { nanoid } from 'nanoid'

function formatModel(model) {
    let formatted = {}
    let nodes = [] 
    model.forEach(node => {
        let formattedNode = { 
            id: node.id, 
            group: node.group, 
            type: node.type, 
            sources: node.sourceNodes.map(sc => sc.id)
        }
        let params = []
        Object.keys(node.paramsData).forEach(param => {
            params.push({ id: param, value: node.paramsData[param]})
        })
        formattedNode['params'] = params
        nodes.push(formattedNode)
    })
    formatted['nodes'] = nodes
    return formatted
}

const defaultSettings = {
  name: '',
  description: '',
  client: '',
  contexts: [],
  tags: [],
  interval: '1h',
  model: [],
  saveId: undefined,
}

const state = {
  all: [],
  local: [],
  //activeAnalysis: {},
  activeAnalysisId: '',
  results: [],
  activeAnomalyId: '',
}

const getters = {
    getAnalysisById: (state) => (id) => {
        let item = state.local.find(elem => elem.id == id)
        return item ? item : {}
    },
    getResultsById: (state) => (id) => {
        let item = state.results.find(elem => elem.id == id)
        return item ? item : {}
    },

    activeAnalysis: (state) => {
        console.log("getter triggers")
        let found = state.local.find(elem => elem.id == state.activeAnalysisId)
        console.log(found)

        return found ? found : {}
    },
 /* getAnomalies: (state) => {
        if ((state.results.hasOwnProperty('anomalies') 
        && Array.isArray(state.results.anomalies) 
        && state.results.anomalies.length)) {
            return state.results.anomalies
        } else {
            return []
        }
    },
    getAnomalyById: (state) => (id) => {
        if ((state.results.hasOwnProperty('anomalies') 
        && Array.isArray(state.results.anomalies) 
        && state.results.anomalies.length)) {
            return state.results.anomalies.find(item => item.id === id)
        }
    } */
}

const mutations = {
    set_all_analysis(state, payload) {
        state.all = payload
    },
    add_analysis(state, payload) {
        state.local.push(payload)
    },
    set_active(state, id) {
        let found = state.local.find(elem => elem.id == id)
        if (found) {
            state.activeAnalysisId = id
        } else {
            state.activeAnalysis = ''
        }
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
    },
    add_results(state,  {id, loading, results}) {
        results.id = id
        results.loading = loading
        if (results.hasOwnProperty('anomalies') && results.anomalies.length > 0) {
            var anoms = []
            for (var item of results.anomalies) {
                anoms.push({
                        id: nanoid(6),
                        from: item.from,
                        to: item.to,
                       // color: getColorByvalue(item.score/100),
                        score: item.score,
                })
            }
            results.anomalies = anoms
        }
        let index = state.results.findIndex(elem => elem.id == id)
        if (index > -1) {
            state.results.splice(index, 1, results)
        } else {
            state.results.push(results)
        } 
    },
    set_active_anomaly(state, anomalyId) {
        state.activeAnomalyId = anomalyId
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
                    let loaded = response.data
                    let settings = {}
                    settings.saveId = loaded.id
                    settings.id = nanoid(5)
                    settings.name = loaded.name
                    settings.description = loaded.description
                    settings.client = loaded.data_options.client
                    settings.tags = loaded.data_options.tags
                    settings.contexts = loaded.data_options.contexts
                    settings.interval = loaded.data_options.interval
                    settings.model = loaded.model
                    store.commit('add_analysis', settings)
                    store.commit('set_active', settings.id)
                })
                .catch(error => console.log())
    }, 
    saveAnalysis({commit, getters, dispatch}, {id, name, description}) {
        const settings = getters.getAnalysisById(id)
        const objectToSave = { 
            client: settings.client,
            name: name,
            description: description,
            data_options: { 
                client: settings.client, 
                tags: settings.tags, 
                contexts: settings.contexts, 
                interval: settings.interval
            },
            model: settings.model 
        }
        return  api.addNewAnalysis(objectToSave)
                .then(response => {
                    const saveId = response.data.id
                    commit('update_analysis', {id, name, description, saveId})
                    commit('set_active', id)
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
            data_options: { 
                client: settings.client, 
                tags: settings.tags, 
                contexts: settings.contexts, 
                interval: settings.interval
            },
            model: settings.model 
        }
        return  api.updateAnalysis(objectToSave, settings.saveId)
                .then(response => {
                    commit('update_analysis', {id, name, description})
                    commit('set_active', id)
                    dispatch("fetchAllAnalysis")
                })
                .catch(error => console.log(error))

    },
    deleteAnalysis({dispatch}, id) {
        return  api.deleteAnalysis(id)
                .then(response => dispatch("fetchAllAnalysis"))
                .catch(error => console.log(error))
    },
  /*  deleteAnalysisList({dispatch}, idList) {
        return  api.deleteAnalysis(idList)
                .then(response => dispatch("fetchAllAnalysis"))
                .catch(error => console.log(error))
    }, */
    createLocalAnalysis(store) {
        const newId = nanoid(5)
        store.commit('add_analysis', { id: newId, ...defaultSettings })
        store.commit('set_active', newId)
    },
    closeLocalAnalysis(store, id) {
        store.commit('remove_analysis', id)
    },
    updateLocalSettings(store, settings) {
        console.log(settings)
        store.commit('update_analysis', settings)
    },
	runAnalysis({commit, getters}, id) {
        let settings = getters.getAnalysisById(id)
        if (Object.keys(settings).length == 0) return
        commit('add_results', {id: id, loading: true, results: {} })
        return  api.getAnomalies({
                    name: settings.client,
                    tags: settings.tags,
                    contexts: settings.contexts,
                    interval: settings.interval,
                    model: formatModel(settings.model)
                })
                .then(response => {       
                    commit('add_results', {id: id, loading: false, results: response.data}) 
                })
                .catch(error => { 
                    console.log('error retrieving analysis')
                })         
    },
    setActiveAnalysis(store, id) {
        store.commit('set_active', id)
    },
    setActiveAnomaly(store, id) {
        store.commit('set_active_anomaly', id)
    },
}


export default {
    namespaced: true,
    getters,
    state,
    mutations,
    actions,
}