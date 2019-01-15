const state = {
  clients: [],
  tags: [],
  contexts: [],
  range: {
    start: null,
    end: null
  },

  series: {},
  activeSeries: {},


  anomalies: [],
  loading: null,
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
    update_clients(state, payload) {
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
    set_start_date(state, payload) {
        state.range.start = payload
    },
    set_end_date(state, payload) {
        state.range.end = payload
    },
    set_anomalies(state, payload) {
        state.anomalies = payload
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

//hosturl = 'http://localhost:8000/prueba/'

const actions = {
    fetchClients(store) {
        return axios.get('http://localhost:8000/prueba/clients/')
        .then(response => {       
          store.commit('update_clients', response.data) 

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
    fetchData(store, settings) {
        // sets `state.loading` to true. Show a spinner or something.
        console.log('data pending')

        let requested = state.series[settings.name]


        return axios.get('http://localhost:8000/prueba/series/', {
                params: {
                  name: requested.client,
                  tags: requested.tags,
                  contexts: requested.contexts,
                  start: state.range.start,
                  end: state.range.end,
/*                  interval: state.displayInterval
*/                }
        })
        .then(response => {       
          // sets `state.loading` to false 
          // also sets `state.apiData to response`
          store.commit('add_data', {name: settings.name, data: response.data}) 
        })
        .catch(error => { 
          // set `state.loading` to false and do something with error   
          console.log('error loading series data')
        })
    },
    fetchAnomalies(store) {
        return axios.get('http://localhost:8000/prueba/anomalies/', {
                params: {
                  name: state.clientName,
                  tags: state.clientTags,
                  contexts: state.clientContext,
                  start: state.range.start,
                  end: state.range.end
                }
        })
        .then(response => {       
          store.commit('set_anomalies', response.data) 
        })
        .catch(error => { 
          console.log('error retrieving anomalies')
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
        store.dispatch("fetchData", seriesOptions)
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
/*        state.series[name] = { ...state.series[name], ...rest }
*/      store.commit("update_series", seriesOptions)
        if (updateData) {
            store.dispatch("fetchData", seriesOptions)
        }
    },
    changeSeriesActiveStatus(store, seriestatus) {
        store.commit('set_active_series', seriestatus)
    }

}

export default {
  state,
  getters,
  actions,
  mutations
}