const state = {
  clients: [],
  data: [],
  anomalies: [],
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
  loading: null
}

const namespaced = true

const mutations = {
    update_clients(state, payload) {
        state.clients = payload
    },
    add_data(state, payload) {
        state.data = payload
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
    fetchData(store) {
        // sets `state.loading` to true. Show a spinner or something.
         console.log('data pending')

        return axios.get('http://localhost:8000/prueba/series/', {
                params: {
                  name: state.clientName,
                  tags: state.clientTags,
                  contexts: state.clientContext,
                  start: state.range.start,
                  end: state.range.end,
                  interval: state.displayInterval
                }
        })
        .then(response => {       
          // sets `state.loading` to false 
          // also sets `state.apiData to response`
          store.commit('add_data', response.data) 
        })
        .catch(error => { 
          // set `state.loading` to false and do something with error   
          console.log('error loading series data')
        })
    },
    fetchContexts(store) {
        return axios.get('http://localhost:8000/prueba/contexts/', {
                params: {
                    name: state.clientName
                }
        })
        .then(response => {
          store.commit('set_contexts', response.data) 
        })
        .catch(error => { 
            console.log('error loading contexts data');
        });
    },
    fetchTags(store) {
        return axios.get('http://localhost:8000/prueba/tags/', {
                params: {
                    name: state.clientName
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
    changeCurrentClient(store, data) {
        store.commit("set_current_client", data)
        if (data) {
            store.dispatch('fetchContexts')
            store.dispatch('fetchTags')
        } else {
            store.commit('set_current_tag', '')
            store.commit('set_current_context', '')           
        }
    }
}

export default {
  state,
  actions,
  mutations
}