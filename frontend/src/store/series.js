const state = {
  clients: [],
  tags: [],
  contexts: [],
  range: {
    start: null,
    end: null
  },

  series: {},
  loading: 0,  //using counter instead of boolean for multiple series loading
  activeSeries: {},

  anomalies: [],
}

const namespaced = true

const getters = {
    getSeriesNames: (state) => {
        return Object.keys(state.series)
    },
    getDisplaySeries: (state) => {
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
    }
}


const mutations = {
    set_clients(state, payload) {
        state.clients = payload
    },
    set_tags(state, payload) {
        state.tags = payload
    },
    set_contexts(state, payload) {
        state.contexts = payload
    },
    set_range(state, payload) {
        state.range = payload
    },
    add_series(state, payload) {
        state.series = { ...state.series, ...payload }
    },
    add_data(state, payload) {
        state.series[payload.name] = { ...state.series[payload.name] , data: payload.data }
    },
    add_anomalies(state, payload) {
        state.anomalies = payload
        // let newentry = { [payload.name]: payload.data}
        // state.anomalies = { ...state.anomalies, ...newentry}
            
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

//hosturl = 'http://localhost:8000/prueba/'

const actions = {
    fetchClients(store) {
        return axios.get('http://localhost:8000/prueba/clients/')
        .then(response => {       
          store.commit('set_clients', response.data) 

        })
        .catch(error => { 
          console.log('error loading client data')
        })
    },
    async fetchContexts(store, client) {
        if (!client) {
            store.commit('set_contexts', [])
            return
        } else {
            return axios.get('http://localhost:8000/prueba/contexts/', {
                    params: {
                        name: client
                    }
            })
            .then(response => {
              store.commit('set_contexts', response.data) 
            })
            .catch(error => { 
                console.log('error loading contexts data');
            });

        }
    },
    async fetchTags(store, client) {
        if (!client) {
            store.commit('set_tags', [])
            return
        } else {
            return axios.get('http://localhost:8000/prueba/tags/', {
                    params: {
                        name: client
                    }
            })
            .then(response => {
              store.commit('set_tags', response.data) 
            })
            .catch(error => { 
                console.log('error loading tags data');
            });
        }
    },
    async fetchData(store, name) {
        let requested = state.series[name]
        state.loading += 1
        return axios.get('http://localhost:8000/prueba/series/', {
                params: {
                  name: requested.client,
                  tags: requested.tags,
                  contexts: requested.contexts,
                  start: state.range.start,
                  end: state.range.end,
                  interval: requested.interval
                }
        })
        .then(response => {       
          store.commit('add_data', {name: name, data: response.data}) 
          state.loading -= 1
        })
        .catch(error => { 
          state.loading -= 1
          console.log('error loading series data')
        })
    },
    async updateTagsContexts(store, client) {
        if (client) {
            let tgs = store.dispatch('fetchTags', client) 
            let ctx = store.dispatch('fetchContexts', client)
            let res = [ await tgs, await ctx ]
        } else {
            store.commit('set_tags', [] )
            store.commit('set_contexts', [])           
        }
    },
    addSeries(store, seriesOptions) {
        let { name, ...rest} = seriesOptions
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
        let updateData = false
        if ((rest.client != current.client) || (rest.tags != current.tags) 
            || (rest.contexts != current.contexts) || (rest.interval != current.interval) ) {
            console.log("must fetch data")
            updateData = true
        }
        store.commit("update_series", seriesOptions)
        if (updateData) {
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
    analizeSeries(store, options) {
        let requested = state.series[options.name]
        return axios.get('http://localhost:8000/prueba/anomalies/', {
                params: {
                  name: requested.client,
                  tags: requested.tags,
                  contexts: requested.contexts,
                  start: state.range.start,
                  end: state.range.end,
                  interval: options.interval,
                  config: options.config
                }
        })
        .then(response => {       
          // store.commit('add_anomalies', {name: options.name, data: response.data}) 
          store.commit('add_anomalies', response.data) 
        })
        .catch(error => { 
          console.log('error retrieving anomalies')
        })
    }
}

export default {
  state,
  getters,
  actions,
  mutations
}