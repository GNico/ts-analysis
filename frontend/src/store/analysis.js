import api from "../api/repository";

const state = {
  series: {},
  activeSeries: '',
  data: {},
  anomalies: {},
  defaultOptions: {
    color: '#6fcd98',
    chartType: 'line',
    interval: '1H',
    start: null,
    end: null,
    activeRangeButton: 'btn1',
    showBaseline: true,
    scoreThreshold: 0,
    analysisInterval: '1H',
    config: ''
  },
  loading: false,
}

const getters = {
    getSeriesOptions: (state) => (name) => {
        return (name ? state.series[name] : state.defaultOptions)
    },
    getDisplaySeriesData: (state) => {
        if (state.activeSeries) {
            let { color, interval, chartType, ...rest} = state.series[state.activeSeries]
            let data = state.data
            return { name: state.activeSeries, color, type: chartType, data  }
        } else {
            return null
        }
    },
}

const mutations = {
	add_anomalies(state, payload) {
        state.anomalies = payload
    },
    set_active_series(state, payload) {
        state.activeSeries = payload.active ? payload.name : ''
    },
    add_series(state, payload) {
        state.series = { ...state.series, ...payload } 
    },
    delete_series(state, payload) {
        let { [payload]:name, ...rest } = state.series
        state.series = rest;
        ({ [payload]:name, ...rest } = state.data );
        state.data = rest;
        if (state.activeSeries === payload) {
            state.activeSeries = ''
        }
    },
    set_series_options(state, payload) {
        state.series[payload.name] = { ...state.series[payload.name], ...payload.options }
    },
    set_default_options(state, payload) {
        state.defaultOptions = { ...state.defaultOptions, ...payload.options}
    },

    add_data(state, payload) {
        state.data[payload.name] = { ...state.data[payload.name], ...payload.options }
    }

}

const actions = {
	analizeSeries(store, name) {
        if (name) {
            let targetInfo = store.rootGetters['series/getSeriesOptions'](name)
            let seriesOpts = state.series[name]
            return  api.getAnomalies({
                        name: targetInfo.client,
                        tags: targetInfo.tags,
                        contexts: targetInfo.contexts,
                        start: seriesOpts.start,
                        end: seriesOpts.end,
                        analysisInterval: seriesOpts.analysisInterval,
                        config: seriesOpts.config
                    })
                    .then(response => {       
                        store.commit('add_anomalies', response.data) 
                    })
                    .catch(error => { 
                        console.log('error retrieving analysis')
                    })
        }
    },
    setActiveSeries(store, payload) {
        store.commit("set_active_series", payload)
        if (state.series.hasOwnProperty(payload.name) && !state.data.hasOwnProperty(payload.name)) {
            store.dispatch('fetchSeriesData', payload.name)
        }
    },
    addSeries(store, name) {
        store.commit('add_series', { [name]: state.defaultOptions}) 
    },
    deleteSeries(store, name) {
        store.commit("delete_series", name)
    },
    changeSeriesOptions(store, payload) {
        if (payload.name) {
            store.commit('set_series_options', payload)
        }
        store.commit('set_default_options', payload)
    },
    fetchSeriesData(store, name) {
        if (name) {
            let targetInfo = store.rootGetters['series/getSeriesOptions'](name)
            state.loading = true
            let seriesOpts = state.series[name]
            return  api.getSeriesData({ 
                        name: targetInfo.client,
                        tags: targetInfo.tags,
                        contexts: targetInfo.contexts,
                        start: seriesOpts.start,
                        end: seriesOpts.end,
                        interval: seriesOpts.interval})
                    .then(response => {     
                        state.loading = false
                        store.commit('add_data', {name: name, options: {data: response.data}})
                    })
                    .catch(error => { 
                        state.loading = false
                        console.log('error loading series data')
                    })     
        }
    },
}


export default {
    namespaced: true,
    getters,
    state,
    mutations,
    actions
}