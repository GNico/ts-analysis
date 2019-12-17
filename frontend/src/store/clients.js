import api from "../api/repository";


const state = {
  clients: [],
  tags: [],
  contexts: [],
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
  async fetchContexts(store, client) {
      if (!client) {
          store.commit('set_contexts', [])
          return
      } else {
          return  api.getContexts(client)
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
          return  api.getTags(client)
                  .then(response => {
                    store.commit('set_tags', response.data) 
                  })
                  .catch(error => { 
                      console.log('error loading tags data');
                  });
      }
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
}


export default {
  namespaced: true,
  state,
  actions,
  mutations
}