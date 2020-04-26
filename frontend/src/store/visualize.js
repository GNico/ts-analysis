import api from "../api/repository";
import getFixedSizeArray from "../common/fixedSizeArray"


const colors = ['#2b908f', '#90ee7e', '#f45b5b', '#7798BF', '#aaeeee', '#ff0066',
        '#eeaaee', '#55BF3B', '#DF5353', '#7798BF', '#aaeeee']


const state = {
    series: [],
    loading: 0,
    range: {
        start: null,
        end: null
    },

}

const getters = {
    nextColor: state => {
        let index = state.series.length % colors.length 
        return colors[index]
    }
}


const mutations = {
    add_series(state, payload) {
        state.series = { ...state.series, ...payload }
    },
    add_data(state, payload) {
        state.series[payload.id] = { ...state.series[payload.id] , data: payload.data }
    },
    delete_series(state, payload) {
        let { [payload]:id, ...rest} = state.series
        state.series = rest 
    },
    set_range(state, payload) {
        state.range = payload
    }

}


const actions = {
    addSeries({commit, dispatch, getters}, seriesOptions) {
        let id = 'nanoid'
        seriesOptions.color = getters.nextColor
        let newseries = { [id]: seriesOptions } 
        commit("add_series", newseries)
        dispatch("fetchData", id)
    },
    fetchData({commit, state}, id) {
        let seriesOptions = state.series[id]
        state.loading += 1
        return  api.getSeriesData({ 
                    name: seriesOptions.client,
                    tags: seriesOptions.tags,
                    contexts: seriesOptions.contexts,
                    start: state.range.start,
                    end: state.range.end,
                    interval: seriesOptions.interval})
                .then(response => {       
                    commit('add_data', {id: id, data: response.data}) 
                    state.loading -= 1
                })
                .catch(error => { 
                    state.loading -= 1
                    console.log('error loading series data')
                })        
    },
    deleteSeries({commit}, id) {
        commit("delete_series", id)
    },
    updateRange({commit}, range) {
        commit("set_range", range)
    },


}

export default {
    namespaced: true,
    state,
    getters,
    mutations,
    actions,
}


/*const state = {
  

  range: {
    start: null,
    end: null
  },
  series: {},
  loading: 0,  //using counter instead of boolean to track multiple series
  activeSeries: {},
}

const getters = {
    getSeriesNames: (state) => {
        return Object.keys(state.series)
    },
    getDisplaySeriesData: (state) => {
        let activeNames = Object.keys(state.series).filter(item => state.activeSeries[item])
        return activeNames.map(function(itemName) {
                            let { color, chartType, data, ...rest} = state.series[itemName]                
                            return { name: itemName, color, type: chartType, data }
                        })
    },
    getSeriesOptions: (state) => (name) => {
        if (!(name in state.series) ) {
            return {name: '',
                    color: '#6fcd98',
                    chartType: 'line',
                    client: '',
                    contexts: '',
                    tags: '',
                    interval: '1H'}
        }
        else {
            let { data, ...rest} = state.series[name]
            return rest
        }
    },
}


const mutations = {
    set_range(state, payload) {
        state.range = payload
    },
    add_series(state, payload) {
        state.series = { ...state.series, ...payload }
    },
    add_data(state, payload) {
        state.series[payload.name] = { ...state.series[payload.name] , data: payload.data }
    },
    set_active_series(state, payload) {
        state.activeSeries = { ...state.activeSeries, ...payload }
    },
    delete_series(state, payload) {
        let { [payload]:name, ...rest} = state.series
        state.series = rest 
        let { [payload]:name2, ...rest2} = state.activeSeries
        state.activeSeries = rest2
    },
    update_series(state, payload) {
        let { name, ...rest} = payload
        state.series[name] = { ...state.series[name], ...rest }
    },

}


const actions = {
    fetchData(store, name) {
        let targetData = store.rootGetters['series/getSeriesOptions'](name)
        let displayData = state.series[name]
        state.loading += 1
        return  api.getSeriesData({ 
                    name: targetData.client,
                    tags: targetData.tags,
                    contexts: targetData.contexts,
                    start: state.range.start,
                    end: state.range.end,
                    interval: displayData.interval})
                .then(response => {       
                    store.commit('add_data', {name: name, data: response.data}) 
                    state.loading -= 1
                })
                .catch(error => { 
                    state.loading -= 1
                    console.log('error loading series data')
                })        
    },
    addSeries(store, seriesOptions) {
        let { name, ...rest} =  seriesOptions
        let newseries = { [name]: rest }
        store.commit("add_series", newseries)
        store.commit("set_active_series", { [name]: true })
        store.dispatch("fetchData", name)
    },
    deleteSeries(store, seriesName) {
        store.commit("delete_series", seriesName)
    },
    updateSeries(store, seriesOptions) {
        let { name, ...rest} = seriesOptions
        let current = state.series[name]
        store.commit("update_series", seriesOptions)
        if (rest.interval != current.interval) {
            store.dispatch("fetchData", name)
        }
    },
    changeSeriesActiveStatus(store, seriestatus) {
        store.commit('set_active_series', seriestatus)
    },

    updateRange(store, range) {
        store.commit("set_range", range)
        Object.keys(state.series).forEach(key => {
            store.dispatch('fetchData', key)
        })
    },
    setActiveSeries(store, payload) {
        store.commit("set_active_series", payload)
    }
}

export default {
    namespaced: true,
    state,
    getters,
    mutations,
    actions,
}

*/