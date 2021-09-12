import api from "../api/repository";

const state = {
  clients: [],
  details: {},
  tags: {},
  contexts: {},
}

const getters = {
  readyClients: state => {
    return state.clients.filter(item => item.status == 'Ready').map(item => item.name)
  },
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
  set_details(state, {name, details}) {
    state.details = { ...state.details, ...{[name]: details}  }
  },
  add_tags(state, {client, tags}) {
    state.tags = { ...state.tags, [client]: tags }
  },
  add_contexts(state, {client, contexts}) {
    state.contexts = { ...state.contexts, [client]: contexts }
  },
}


const actions = {
  addClient(store, form) {
    return  api.addNewClient({
              name: form.name,
              folder_name: form.folderName,
              utc_offset: form.UTCOffset
            })
            .then(response => {})
            .catch(error => { 
              console.log('error creating new client')
            })
  },
  deleteClient(store, name) {
    return  api.deleteClient(name)
  },
  fetchClients(store) {
    return  api.getClients()
            .then(response => {       
              store.commit('set_clients', response.data) 
            })
            .catch(error => { 
              console.log('error loading client data')
              console.log(error)
            })
  },
  fetchClientDetails(store, name) {
    return  api.getClientDetails(name)
            .then(response => {       
              store.commit('set_details', {name: name, details: response.data}) 
            })
  }, 
  fetchTags(store, client) {
    if (client) {
      return  api.getTags(client)
            .then(response => {
              store.commit('add_tags', {client, tags: response.data})
            })
            .catch(error => { 
                console.log('error loading tags data')
            })
    }
  },
  fetchContexts(store, client) {
    if (client) {
      return  api.getContexts(client)
            .then(response => {
              store.commit('add_contexts', {client, contexts: response.data})
            })
            .catch(error => { 
                console.log('error loading contexts data')
            })
    }
  },
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}