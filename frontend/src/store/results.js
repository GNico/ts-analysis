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

function formatAnomalies(anomalies) {
    var anoms = []
    for (var item of anomalies) {
        anoms.push({
            id: nanoid(8),
            from: item.from,
            to: item.to,
            score: item.score,
        })
    }
    return anoms
}

const state = {
  all: {},
  activeResultsId: '',
  activeAnomalyId: '',
}

const getters = {
    getResultsById: (state) => (id) => {
        let item = state.results.find(elem => elem.id == id)
        return item ? item : {}
    }, 
    activeResults: (state, getters) => {
        return state.all[state.activeResultsId]
    },


}

const mutations = {    
    set_active_results(state, id) {
        state.activeResultsId = id
    },
    add_results(state, payload) {

    },
    remove_results(state, id) {
        if (state.all.hasOwnProperty(id)) {
            let { id, ...newResults } = state.all
            state.all = newResults
        }
    },
    set_active_anomaly(state, anomalyId) {
        state.activeAnomalyId = anomalyId
    },
    add_results(state,  {id, taskId, loading, results}) {
        if (results.hasOwnProperty('anomalies') && results.anomalies.length > 0) {
            results.anomalies = formatAnomalies(results.anomalies)
        }
        let newResults = {id, taskId, loading, results }
        state.all = { ...state.all, [id]: newResults }
    },
}

const actions = {    
    setActiveAnomaly(store, id) {
        store.commit('set_active_anomaly', id)
    },
    startAnalysis({commit, getters}, settings) {
        if (!settings) return
        commit('add_results', {id: settings.id, loading: true, taskId: undefined, results: {} })
        return  api.getAnomalies({
                    client: settings.client,
                    tags: settings.tags,
                    contexts: settings.contexts,
                    interval: settings.interval,
                    model: formatModel(settings.model)
                })
                .then(response => {    
                    commit('add_results', {id: settings.id, loading: true, taskId: response.data.task_id, results: {} }) 
                })
                .catch(error => { 
                    console.log('error performing analysis')
                    console.log(error)
                })         
    },
    fetchResults({commit, getters}, id) {
        let results = getters.activeResults
        if (results.loading && results.hasOwnProperty('taskId') && results.taskId) {
            api.getResults(results.taskId)
            .then(response => {
                if (response.data.state == 'success' || response.data.state == 'failed')
                    commit('add_results', {id: results.id, loading: false, taskId: undefined, results: response.data.result })
            })
            .catch(error => { 
                console.log('error fetching results')
                console.log(error)

            }) 
        }
    },
    
}


export default {
    namespaced: true,
    getters,
    state,
    mutations,
    actions,
}