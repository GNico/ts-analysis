import api from "../api/repository";
import { nanoid } from 'nanoid'

const colors = ['#f45b5b', '#90ee7e', '#7798BF', '#aaeeee', '#ff0066',
        '#eeaaee', '#55BF3B', '#DF5353', '#7798BF', '#aaeeee', '#2b908f']

//returns a deep copy of the series object 
function makeSeriesOptionsCopy(seriesOptions) {
    let newSeriesOptions = { ...seriesOptions }
    newSeriesOptions.tags = [ ...seriesOptions.tags ]
    newSeriesOptions.contexts = [ ...seriesOptions.contexts ]
    return newSeriesOptions
}

function compareArrays(array1, array2) {
    return (array1.length === array2.length) && (array1.sort().every((value, index) => value === array2[index]))
}

const state = {
    series: {},
    seriesIds: [],
    panels: [],
    range: {
        start: null,
        end: null
    },
    loading: 0,
    settings: {},
    allSeriesRange: {
        start: null,
        end: null
    }
}

const getters = {
    seriesAsList: state => {
        return state.seriesIds.map(id => state.series[id])
    },
    seriesNames: state => {
        return state.seriesIds.map(id => state.series[id].name)
    }, 
    getSeriesById: state => id => {
        return (id && state.series.hasOwnProperty(id)) ? makeSeriesOptionsCopy(state.series[id]) : null
    },
    nextColor: state => {
        let index = state.seriesIds.length % colors.length 
        return colors[index]
    },
    numPanels: state => {
        return state.panels.length ? state.panels.length : 1
    },
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
    update_series(state, seriesOptions) { 
        state.series[seriesOptions.id] = { ...state.series[seriesOptions.id], ...seriesOptions }
    },
    set_range(state, {start, end}) {
        state.range.start = start
        state.range.end = end
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
        if (state.series.hasOwnProperty(payload.id)) {
            state.series[payload.id] = { ...state.series[payload.id], ...newaxis } 
        }
    },
    delete_series_from_panel(state, id) {
        let axisNumber = state.series[id].yAxis
        let seriesIndex = state.panels[axisNumber].indexOf(id)
        if (seriesIndex != -1) { 
            state.panels[axisNumber].splice(seriesIndex, 1)
            //delete panel if empty 
            if (state.panels[axisNumber].length == 0) {
                state.panels.splice(axisNumber, 1)
                //update new panel number on remaining series 
                for (let i = axisNumber; i < state.panels.length; i++) {
                    state.panels[i].forEach(function(item) {
                        if (state.series.hasOwnProperty(item)) {
                            let newaxis = { yAxis: i}
                            state.series[item] = { ...state.series[item], ...newaxis}
                        }
                    })
                }
            }    
        }
    },
    move_series(state, {id, offset}) {
        let axisNumber = state.series[id].yAxis
        let seriesIndex = state.panels[axisNumber].indexOf(id)
        if (seriesIndex != -1) { 
            //remove series from panel
            state.panels[axisNumber].splice(seriesIndex, 1)  
            //add series to new panel
            const newAxisNumber = axisNumber + offset
            let newaxis = {}
            if (newAxisNumber < 0 || newAxisNumber > state.panels.length-1) {
                state.panels.push([id])
                newaxis['yAxis'] = state.panels.length-1
            } else {
                state.panels[newAxisNumber].push(id)
                newaxis['yAxis'] = parseInt(newAxisNumber)
            }   
            if (state.series.hasOwnProperty(id)) {
                state.series[id] = { ...state.series[id], ...newaxis } 
            }
            //remove leftover empty arrays
            if (state.panels[axisNumber].length == 0) {
                state.panels.splice(axisNumber, 1)
                //update new panel number on remaining series 
                for (let i = axisNumber; i < state.panels.length; i++) {
                    state.panels[i].forEach(function(item) {
                        if (state.series.hasOwnProperty(item)) {
                            let newaxis = { yAxis: i}
                            state.series[item] = { ...state.series[item], ...newaxis}
                        }
                    })
                }
            }    
        }
    },
    set_settings(state, newSettings) {
        state.settings = { ...newSettings }
    },
    adjust_all_series_range(state) {
        if (state.range.start && state.range.end) {
            state.allSeriesRange = state.range            
        } else {
            let axisMin = state.range.start
            let axisMax = state.range.end
            state.seriesIds.forEach(seriesId => {
                let seriesData = state.series[seriesId].data
                let currentMin = seriesData[0][0]
                let currentMax = seriesData[seriesData.length -1][0]
                if (!state.range.start) {
                     if (!axisMin || axisMin > currentMin) {
                        axisMin = currentMin
                    }
                } 
                if (!state.range.end) {
                     if (!axisMax || axisMax < currentMax) {
                        axisMax = currentMax
                    }
                }
            })
            state.allSeriesRange = { start: axisMin, end: axisMax }
        }       
    }
}

const actions = {
    addSeries({commit, dispatch}, seriesOptions) {
        let newSeriesOptions = makeSeriesOptionsCopy(seriesOptions)
        const newId = nanoid()      
        newSeriesOptions.id = newId
        commit("add_series", newSeriesOptions)
        commit("add_series_to_panel", newSeriesOptions)
        dispatch("fetchData", newId)
    },
    updateSeries({commit, state, dispatch}, {id, seriesOptions} ) {
        seriesOptions.id = id
        const shouldFetchData = 
            (seriesOptions.hasOwnProperty('interval') && (state.series[id].interval != seriesOptions.interval)) ||
            (seriesOptions.hasOwnProperty('client') && (state.series[id].client != seriesOptions.client)) ||
            (seriesOptions.hasOwnProperty('tags') && !compareArrays(state.series[id].tags, seriesOptions.tags)) ||
            (seriesOptions.hasOwnProperty('contexts') && !compareArrays(state.series[id].contexts, seriesOptions.contexts))
        commit("update_series", seriesOptions)
        if (shouldFetchData)
            dispatch("fetchData", id)
    },
    fetchData({commit, state}, id) {
        let seriesOptions = state.series[id]
        commit('set_loading', true)      
        return  api.getSeriesData({ 
                    name: seriesOptions.client,
                    tags: (seriesOptions.tags && seriesOptions.tags.length == 1 && seriesOptions.tags[0] == "root") ? [] : seriesOptions.tags,
                    contexts: (seriesOptions.contexts && seriesOptions.contexts.length == 1 && seriesOptions.contexts[0] == "root") ? [] : seriesOptions.contexts,
                    start: state.range.start ? state.range.start.toISOString() : null ,
                    end: state.range.end ? state.range.end.toISOString() : null,
                    interval: seriesOptions.interval})
                .then(response => {       
                    commit('add_data', {id: id, data: response.data})                     
                    commit('set_loading', false)
                    commit('adjust_all_series_range')
                })
                .catch(error => { 
                    commit('set_loading', false)
                    console.log('error loading series data')
                })        
    },
    deleteSeries({commit}, id) {
        commit("delete_series_from_panel", id)
        commit("delete_series", id)
        commit("adjust_all_series_range")
    },
    updateRange({commit, state, dispatch}, range) {
        commit("set_range", range)
        state.seriesIds.forEach(id =>  dispatch("fetchData", id))
    },
    moveSeriesDown({commit, state}, id) {
        const currentPanel = state.series[id].yAxis        
        if ( !((state.seriesIds.length <= 1) ||     //check for extreme cases where nothing should happen
                ((currentPanel == state.panels.length-1) && 
                    (state.panels[currentPanel].length == 1))) )
            commit("move_series", {id: id, offset: 1})
    },
    moveSeriesUp({commit, state}, id) {
        const currentPanel = state.series[id].yAxis
        if (!((state.seriesIds.length <= 1) || currentPanel == 0))
            commit("move_series", {id: id, offset: -1})
    },
    changeSettings({commit}, newSettings) {
        commit("set_settings", newSettings)
    }
}

export default {
    namespaced: true,
    state,
    getters,
    mutations,
    actions,
}