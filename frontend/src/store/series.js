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
  client_name: '',
  client_context: '',
  client_tags: '',
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
    set_start_date(state, payload) {
        state.range.start = payload
    },
    set_end_date(state, payload) {
        state.range.end = payload
    },
    set_client_name(state, payload) {
        state.client_name = payload
    },
    set_client_context(state, payload) {
        state.client_context = payload
    },
    set_client_tags(state, payload) {
        state.client_tags = payload
    },
    set_anomalies(state, payload) {
        state.anomalies = payload
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
    fetchData(store) {
        // sets `state.loading` to true. Show a spinner or something.
         console.log('data pending')

        return axios.get('http://localhost:8000/prueba/series/', {
                params: {
                  name: state.client_name,
                  tags: state.client_tags,
                  contexts: state.client_context,
                  start: state.range.start,
                  end: state.range.end
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
                    name: state.client_name
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
                    name: state.client_name
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
                  name: state.client_name,
                  tags: state.client_tags,
                  contexts: state.client_context,
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
    }
}

export default {
  state,
  actions,
  mutations
}