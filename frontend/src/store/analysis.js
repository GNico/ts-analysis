import api from "../api/repository";
import { nanoid } from 'nanoid'



const state = {
  /*results: {
    series: [],
    anomalies: [],
    baseline: [],
    trend: []
  }, */
  activeAnomalyId: '',
  loading: false,



  all: [],
  activeAnalysisId: '',
  results: []

}

const getters = {
    getAnalysisById: (state) => (id) => {
        let item = state.all.find(elem => elem.id == id)
        return item ? item : {}
    },
    getResultsById: (state) => (id) => {
        let item = state.results.find(elem => elem.id == id)
        return item ? item : {}
    },

 /*   getAnomalies: (state) => {
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
    add_analysis(state, payload) {
        state.all.push(payload)
        state.activeAnalysisId = payload.id
    },
    set_active(state, id) {
        if (state.all.find(elem => elem.id == id)) {
            state.activeAnalysisId = id
        } else {
            state.activeAnalysisId = ''
        }
    },
    remove_analysis(state, id) {
        let index = state.all.findIndex(elem => elem.id == id)
        if (index > -1) {
            if (state.all[index].id == state.activeAnalysisId)
                state.activeAnalysisId = ''
            state.all.splice(index, 1)
        }
    },
    update_analysis(state, settings) {
        if (settings.hasOwnProperty('id')) {
            let index = state.all.findIndex(elem => elem.id == settings.id)
            if (index > -1) {
                let updated = { ...state.all[index] , ...settings}
                state.all.splice(index, 1, updated)
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
        if (index >= -1) {
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
    createAnalysis(store) {
        store.commit('add_analysis', { id: nanoid(5) })
    },
    setActiveAnalysis(store, id) {
        store.commit('set_active', id)
    },
    removeAnalysis(store, id) {
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
                    //start: seriesOpts.start,
                    //end: seriesOpts.end,
                    interval: settings.interval,
                    //config: seriesOpts.config
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