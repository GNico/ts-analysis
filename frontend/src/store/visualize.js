import api from "../api/repository";
import { nanoid } from 'nanoid'


const colors = [ '#f45b5b', '#90ee7e', '#7798BF', '#aaeeee', '#ff0066',
        '#eeaaee', '#55BF3B', '#DF5353', '#7798BF', '#aaeeee', '#2b908f']

const state = {
    series: {},
    seriesIds: [],
    panels: [],
    range: {
        start: null,
        end: null
    },
    loading: 0,

}

const getters = {
    seriesAsList: state => {
        return state.seriesIds.map(id => state.series[id])
    },
    seriesNames: state => {
        return state.seriesIds.map(id => state.series[id].name)
    }, 
    getSeriesById: state => id => {
        return (id && state.series.hasOwnProperty(id)) ? state.series[id] : null
    },
    nextColor: state => {
        let index = state.seriesIds.length % colors.length 
        return colors[index]
    },
    numPanels: state => {
        return state.panels.length ? state.panels.length : 1
    }

}


const mutations = {
    add_series(state, payload) {
        state.seriesIds.push(payload.id)
        let newseries = { [payload.id]: payload }
        state.series = { ...state.series, ...newseries }
    },
    add_data(state, payload) {
        state.series[payload.id] = { ...state.series[payload.id] , data: payload.data }
    },
    delete_series(state, id) {
        let { [id]:theId, ...rest} = state.series
        state.series = rest
        let index = state.seriesIds.indexOf(id);
        if (index !== -1)  state.seriesIds.splice(index, 1);
    },
    update_series(state, payload) { 
        state.series[payload.id] = { ...state.series[payload.id], ...payload.seriesOptions }
    },
    set_range(state, payload) {
        state.range = payload
    },
    set_loading(state, isLoading) {
        if (isLoading) 
            state.loading += 1;
        else 
            state.loading -= 1;
    },


    add_series_to_panel(state, payload) {
        let axisNumber = (!payload.hasOwnProperty("yAxis")) ? -1 : payload.yAxis
        let newaxis = {}
        if (axisNumber < 0 || axisNumber > state.panels.length-1) {
            state.panels.push([payload.id])
            newaxis['yAxis'] = state.panels.length-1
        } else {
            state.panels[axisNumber].push(payload.id)
            newaxis['yAxis'] = parseInt(axisNumber)
        }
        state.series[payload.id] = { ...state.series[payload.id], ...newaxis } 
    },
    delete_series_from_panel(state, id) {
        var shiftArray = false
        for (var panelIndex = 0; panelIndex < state.panels.length; panelIndex++) { 
            if (shiftArray) {
                state.panels[panelIndex].forEach(series_id => state.series[series_id].yAxis -= 1 )
            } else {
                let index = state.panels[panelIndex].indexOf(id)
                if (index !== -1) {
                    state.panels[panelIndex].splice(index, 1)
                    if (!state.panels[panelIndex].length) 
                        state.panels.splice(panelIndex, 1) 
                        shiftArray = true
                        panelIndex -= 1
                } 
            }
        }  
    },



}


const actions = {
    addSeries({commit, dispatch, getters}, seriesOptions) {
        let id = nanoid()      
        seriesOptions.color = getters.nextColor
        seriesOptions.id = id
        commit("add_series", seriesOptions)
        commit("add_series_to_panel", seriesOptions)
        dispatch("fetchData", id)
    },
    fetchData({commit, state}, id) {
        let seriesOptions = state.series[id]
        commit('set_loading', true)
        return  api.getSeriesData({ 
                    name: seriesOptions.client,
                    tags: seriesOptions.tags,
                    contexts: seriesOptions.contexts,
                    start: state.range.start,
                    end: state.range.end,
                    interval: seriesOptions.interval})
                .then(response => {       
                    commit('add_data', {id: id, data: response.data}) 
                    commit('set_loading', false)
                })
                .catch(error => { 
                    commit('set_loading', false)
                    console.log('error loading series data')
                })        
    },
    deleteSeries({commit}, id) {
        commit("delete_series", id)
        commit("delete_series_from_panel", id)
    },
    updateSeries({commit}, payload) {
        commit("update_series", payload)
    },
    updateRange({commit}, range) {
        commit("set_range", range)
    },
    moveSeriesDown({commit}, id) {

    },
    moveSeriesUp({commit}, id) {

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