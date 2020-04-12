import api from "../api/repository";


const state = {
  clients: [],
  details: {},
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
  set_details(state, payload) {
    state.details = payload
  }
}


const actions = {
  addClient(store, form) {
    return  api.addNewClient(form)
            .then(response => {       
            })
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
              store.commit('set_details', response.data) 
            })
  },  
}


export default {
  namespaced: true,
  state,
  actions,
  mutations
}