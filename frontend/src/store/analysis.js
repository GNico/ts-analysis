import api from "../api/repository";
import { nanoid } from 'nanoid'

function formatModel(model) {
    let formatted = []
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
        formatted.push(formattedNode)
    })
    console.log(formatted)
    return formatted
}



const state = {
  all: [],
  local: [],
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
        state.activeAnalysisId = payload.id
    },
    set_active(state, id) {
        if (state.local.find(elem => elem.id == id)) {
            state.activeAnalysisId = id
        } else {
            state.activeAnalysisId = ''
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
                .then(response => 
                    store.commit('set_all_analysis', response.data))
                .catch(error =>
                    console.log('error fetching analysis list'))
    },
    loadAnalysis(store, saveId) {
        return  api.getAnalysisDetails(saveId)
                .then(response => {
                    let settings = response.data
                    settings.savedId = settings.id
                    settings.id = nanoid(5)
                    settings.client = settings.data_options.client
                    settings.tags = settings.data_options.tags
                    settings.contexts = settings.data_options.contexts
                    settings.interval = settings.data_options.interval
                    console.log(settings)
                    store.commit('add_analysis', settings)
                })
    }, 
    saveAnalysis({store, getters}, id) {
        const settings = getters.getAnalysisById(id)
        const objectToSave = { 
            client: settings.client,
            name: settings.name,
            description: settings.description,
            data_options: { 
                client: settings.client, 
                tags: settings.tags, 
                contexts: settings.contexts, 
                interval: settings.interval
            },
            model: settings.model 
        }
        if (settings.saveId) {
            api.updateAnalysis(objectToSave, savedId).then(response => console.log(response)).catch(error => console.log(error))
        } else {
            api.addNewAnalysis(objectToSave).then(response => console.log(response)).catch(error => console.log(error))
        }
        
    },



    createLocalAnalysis(store) {
        store.commit('add_analysis', { id: nanoid(5), saveId: undefined })
    },
    setActiveAnalysis(store, id) {
        store.commit('set_active', id)
    },
    closeLocalAnalysis(store, id) {
        store.commit('remove_analysis', id)
    },
    updateSettings(store, settings) {
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