import api from "../api/repository";

function getColorByScore(score) {
    let ratio = score/100;
    console.log(ratio)
    let color1 = ''
    let color2 = ''
    if (ratio<0.5) {
    ratio = ratio*2
    color1 = 'ffff00' //centro
    color2 = '00ff00' //left
    } else {
    ratio = (ratio-0.5)*2
    color1 = 'ff0000'  //right
    color2 = 'ffff00' //center
    }
    var hex = function(x) {
      x = x.toString(16);
      return (x.length == 1) ? '0' + x : x;
    };
    var r = Math.ceil(parseInt(color1.substring(0,2), 16) * ratio + parseInt(color2.substring(0,2), 16) * (1-ratio));
    var g = Math.ceil(parseInt(color1.substring(2,4), 16) * ratio + parseInt(color2.substring(2,4), 16) * (1-ratio));
    var b = Math.ceil(parseInt(color1.substring(4,6), 16) * ratio + parseInt(color2.substring(4,6), 16) * (1-ratio));

    return  hex(r) + hex(g) + hex(b);
}


const state = {
  series: {},
  activeSeries: '',
  data: {},
  analysis: {},
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
        if (state.activeSeries && state.data[state.activeSeries]) {
            let { color, interval, chartType, ...rest} = state.series[state.activeSeries]
            let data = state.data[state.activeSeries]
            return { name: state.activeSeries, color, type: chartType, data  }
        } else {
            return []
        }
    },
    getDisplayAnomalies: (state) => {
        if (state.activeSeries && state.analysis[state.activeSeries]) {
            var anoms = []
            for (var item of state.analysis[state.activeSeries].anomalies) {
                anoms.push({
                    from: item.from,
                    to: item.to,
                    color: '#' + getColorByScore(item.score)
                })
            }
            return anoms
        } else {
            return []
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
        state.analysis = { ...state.analysis, ...payload }
    },

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
                        store.commit('add_analysis', {[name]: response.data}) 
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
    actions
}