import api from "../api/repository";



//returns color from a tricolor gradient according to a 0 to 1 value
function getColorByvalue(value) {
    let color1 = ''
    let color2 = ''
    if (value<0.5) {
    value = value*2
    color1 = 'e4e814' //center - yellow
    color2 = '00ff00' //left - green
    } else {
    value = (value-0.5)*2
    color1 = 'db1313'  //right - red
    color2 = 'e4e814' //center - yellow
    }
    var hex = function(x) {
      x = x.toString(16);
      return (x.length == 1) ? '0' + x : x;
    };
    var r = Math.ceil(parseInt(color1.substring(0,2), 16) * value + parseInt(color2.substring(0,2), 16) * (1-value));
    var g = Math.ceil(parseInt(color1.substring(2,4), 16) * value + parseInt(color2.substring(2,4), 16) * (1-value));
    var b = Math.ceil(parseInt(color1.substring(4,6), 16) * value + parseInt(color2.substring(4,6), 16) * (1-value));
    return  '#' + (hex(r) + hex(g) + hex(b));
}

const state = {
  series: {},
  activeSeries: '',
  activeAnomaly: '',
  data: {},
  analysis: {},
  defaultOptions: {
    color: '#3fb0ff',
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
        if (state.activeSeries && state.data[state.activeSeries]) {
            let { color, interval, chartType, ...rest} = state.series[state.activeSeries]
            let data = state.data[state.activeSeries]
            return {name: state.activeSeries, color, type: chartType, data} 
        } else {
            return null
        }
    },
    getDisplayBaseline: (state) => {
        if (state.activeSeries && state.analysis[state.activeSeries]) {
            return  {   data: state.analysis[state.activeSeries].baseline, 
                        type: 'arearange', 
                        color: state.series[state.activeSeries].color,
                        lineWidth: 0,
                        fillOpacity: 0.3,
                        marker: { enabled: false },
                        showInLegend: false,
                        states: {
                            hover: {
                                enabled: false
                            }
                        },
                        enableMouseTracking: false
                    }
        } else {
            return null
        }
    },
    getDisplayAnomalies: (state) => {
        if (state.activeSeries && state.analysis[state.activeSeries]) {
            return state.analysis[state.activeSeries].anomalies.filter(item => item.score >= state.series[state.activeSeries].scoreThreshold)
        } else {
            return []
        }
    },
    getAnomalyById: (state) => (id) => {
        if (state.activeSeries && state.analysis[state.activeSeries]) {
            return state.analysis[state.activeSeries].anomalies.find(item => item.id === id)
        }
    }
}

const mutations = {
    set_active_series(state, payload) {
        state.activeSeries = payload.active ? payload.name : ''
    },
    add_series(state, payload) {
        state.series = { ...state.series, ...payload } 
    },
    delete_series(state, payload) {
        let { [payload]:name, ...rest } = state.series
        state.series = rest;
        ({ [payload]:name, ...rest } = state.data);
        state.data = rest;
        ({ [payload]:name, ...rest } = state.analysis);
        state.analysis = rest;
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
        state.data = { ...state.data, ...payload }
    },
    add_analysis(state, payload) {
        state.analysis = { ...state.analysis, ...{[payload.name]: payload.analysis} }
        //add an id and color to each anomaly for UI purposes
        var anoms = []
        var idx = 0
        for (var item of state.analysis[payload.name].anomalies) {
            anoms.push({
                    id: idx,
                    from: item.from,
                    to: item.to,
                    color: getColorByvalue(item.score/100),
                    score: item.score,
                })
            idx++
        }
        state.analysis[payload.name].anomalies = anoms
    },
    set_active_anomaly(state, payload) {
        state.activeAnomaly = payload
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
                        store.commit('add_analysis', {name: name, analysis: response.data}) 
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
    setActiveAnomaly(store, id) {
        store.commit('set_active_anomaly', id)
    },
    addSeries(store, name) {
        store.commit('add_series', {[name]: state.defaultOptions}) 
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
                        store.commit('add_data', {[name]: response.data})
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
    actions,
}