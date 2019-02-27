import api from "../api/repository";

const state = {
  series: {},
  activeSeries: '',
  defaultOptions: {
    data: [],
    color: '#6fcd98',
    chartType: 'line',
    interval: '1H',
    start: null,
    end: null,
    activeRangeButton: 'btn1',
  },
  loading: false,
}

const getters = {
    getSeriesOptions: (state) => (name) => {
        if (name) {
            return state.series[name]
        } else {
            return state.defaultOptions
        }
    },
    getDisplaySeriesData: (state) => {
        if (state.activeSeries) {
            let { color, interval, chartType, data, ...rest} = state.series[state.activeSeries]
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
        if (payload.active) {
            state.activeSeries = payload.name
        } else {
            state.activeSeries = ''
        }
    },
    add_series(state, payload) {
        state.series = { ...state.series, ...payload } 
    },
    set_series_options(state, payload) {
        state.series[payload.name] = { ...state.series[payload.name], ...payload.options }
    },
    set_default_options(state, payload) {
        state.defaultOptions = { ...state.defaultOptions, ...payload.options}
    }
}

const actions = {
	analizeSeries(store, options) {
        let requested = state.series[options.name]
        return  api.getAnomalies({
                    name: requested.client,
                    tags: requested.tags,
                    contexts: requested.contexts,
                    start: state.range.start,
                    end: state.range.end,
                    interval: options.interval,
                    config: options.config
                })
                .then(response => {       
                    store.commit('add_anomalies', response.data) 
                })
                .catch(error => { 
                    console.log('error retrieving anomalies')
                })
    },
    setActiveSeries(store, payload) {
        store.commit("set_active_series", payload)
    },
    addSeries(store, name) {
        store.commit('add_series', { [name]: state.defaultOptions}) 
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
                        store.commit('set_series_options', {name: name, options: {data: response.data}})
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