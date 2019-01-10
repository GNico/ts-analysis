const state = {
  clients: [],
  tags: [],
  contexts: [],

  range: {
    start: null,
    end: null
  },
  clientName: '',
  clientContext: '',
  clientTags: '',
  displayInterval: '1H',

  series: [],

  anomalies: [],

  displaySeries: [],

  loading: null,
}

const namespaced = true

const getters = {
    getSeriesNames: (state) => {
        return state.series.map(item => item.name)
    },
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
    set_current_client(state, payload) {
        state.clientName = payload
    },
    set_current_context(state, payload) {
        state.clientContext = payload
    },
    set_current_tag(state, payload) {
        state.clientTags = payload
    },
    set_anomalies(state, payload) {
        state.anomalies = payload
    },
    set_display_interval(state, payload) {
        state.displayInterval = payload
    },
    add_series(state, payload) {
        state.series.push( { ...payload } )
    },
    delete_series(state, payload) {
        let index = state.series.findIndex(item => item.name == payload.name)
        state.series.splice(index, 1)
    },
    update_series(state, payload) {
        let index = state.series.findIndex(item => item.name == payload.name)
        state.series[index] = { ...state.series[index], ...payload}
        //state.series.splice(index, 1, payload)
    },
    add_data(state, payload) {
        let index = state.series.findIndex(item => item.name == payload.name)
        state.series[index] = { ...state.series[index], data: payload.data}
        state.displaySeries = state.series.map(item => ({ data: item.data, color: item.color, type: item.chartType}) ) 
    }

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
    fetchData(store, settings) {
        // sets `state.loading` to true. Show a spinner or something.
        console.log('data pending')

        let index = state.series.findIndex(item => item.name == settings.name)
        let requested = state.series[index]


        return axios.get('http://localhost:8000/prueba/series/', {
                params: {
                  name: requested.client,
                  tags: requested.tags,
                  contexts: requested.context,
                  start: state.range.start,
                  end: state.range.end,
/*                  interval: state.displayInterval
*/                }
        })
        .then(response => {       
          // sets `state.loading` to false 
          // also sets `state.apiData to response`
          store.commit('add_data', {name: requested.name, data: response.data}) 
        })
        .catch(error => { 
          // set `state.loading` to false and do something with error   
          console.log('error loading series data')
        })
    },
    fetchContexts(store, client) {
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
    },
    fetchTags(store, client) {
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
    updateTagsContexts(store, client) {
        if (client) {
            store.dispatch('fetchContexts', client)
            store.dispatch('fetchTags', client)
        } else {
            store.commit('set_current_tag', '')
            store.commit('set_current_context', '')           
        }
    },
    addSeries(store, settings) {
        store.commit("add_series", settings)
        store.dispatch("fetchData", settings)
    },
    updateSeries(store, settings) {
        store.commit("update_series", settings)
        store.dispatch("fetchData", settings)
    },
    updateSeriesDisplaySettings(store, settings) {
        store.commit("update_series", settings)
    },

}

export default {
  state,
  getters,
  actions,
  mutations
}