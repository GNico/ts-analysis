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
            sources: node.sourceNodes.map(sc => sc.id),
            debug: true
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

const defaultOptions = {
    activeAnomalyId: '',
    showBaseline: true,
    showSeries: true,
    showTrend: false,
    scoreThreshold: 0,
    minDuration: '',
    minDurationTime: 0,
    selectedRange: {
      start: null,
      end: null
    }
}

const state = {
    all: {},
    activeResultsId: '',
    options: {},
}

const getters = {
    getResultsById: (state) => (id) => {
        let item = state.all[id]
        return item ? item : {}
    }, 
    activeResults: (state) => {
        return state.all[state.activeResultsId]
    },
    activeOptions: (state) => {
        return state.options[state.activeResultsId]
    }
}

const mutations = {    
    set_active_results(state, id) {
        state.activeResultsId = id
    },
    add_results(state, result) {
        if (result.hasOwnProperty('id')) {
            let id = result.id
            let newResult = { ...state.all[id], ...result }
            state.all = { ...state.all, [id]: newResult }
        }
    },
    set_options(state,  options) {
        if (options.hasOwnProperty('id')) {
            let id = options.id
            let newOptions = { ...state.options[id], ...options }
            state.options = { ...state.options, [id]: newOptions }
        }
    },
    remove_results(state, id) {
        if (state.all.hasOwnProperty(id)) {
            let { [id]: _, ...newResults } = state.all
            state.all = newResults
        }
    },
    remove_options(state, id) {
        if (state.options.hasOwnProperty(id)) {
            let { [id]: _, ...newOptions } = state.options
            state.options= newOptions
        }
    },
    set_active_anomaly(state, anomalyId) {
        state.activeAnomalyId = anomalyId
    },

}

const actions = {    
    setActiveAnomaly(store, id) {
        store.commit('set_active_anomaly', id)
    },
    startAnalysis({commit, getters}, settings) {
        if (!settings) return
        commit('add_results', {id: settings.id, loading: true, taskId: undefined })
        commit('set_options', {id: settings.id, ...defaultOptions})
        const model = formatModel(settings.model)
        return  api.getAnomalies({
                    client: settings.client,
                    tags: settings.tags,
                    contexts: settings.contexts,
                    interval: settings.interval,
                    model: model
                })
                .then(response => {    
                    commit('add_results', {id: settings.id, loading: true, taskId: response.data.task_id, model: model }) 
                })
                .catch(error => { 
                    console.log('error performing analysis')
                    console.log(error)
                })         
    },
    fetchResults({commit, getters}, id) {
        let results = getters.getResultsById(id)
        if (results.loading && results.hasOwnProperty('taskId') && results.taskId) {
            api.getResults(results.taskId)
            .then(response => {
                if (response.data.state == 'success')
                    commit('add_results', {id: results.id, loading: false, taskId: response.data.task_id, results: response.data.result, error: '' })
                if (response.data.state == 'failed')
                    commit('add_results', {id: results.id, loading: false, taskId: response.data.task_id, results: {}, error: response.data.error })
            })
            .catch(error => { 
                if (error.response) {
                    commit('add_results', {id: results.id, loading: false, results: {}, error: "An error occurred while performing the analysis"})
                } else if (error.request) {
                    commit('add_results', {id: results.id, loading: false, results: {}, error: "The server could not be reached"})
                } else {
                    commit('add_results', {id: results.id, loading: false, results: {}, error: error.message})
                }
            }) 
        }
    },
    updateOptions(store, payload) {
        store.commit('set_options',  payload)
    },
    deleteResults(store, id) {
        store.commit('remove_results', id)
        store.commit('remove_options', id)
    }
}


export default {
    namespaced: true,
    getters,
    state,
    mutations,
    actions,
}