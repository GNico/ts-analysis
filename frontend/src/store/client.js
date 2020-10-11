const mutations = {
  set_name(state, payload) {
    state.name = payload
  },
  set_tags(state, payload) {
    state.tags = payload
  },
  set_contexts(state, payload) {
    state.contexts = payload
  },
  clear(state) {
    state.name = '',
    state.tags = [],
    state.contexts = []
  })
}

const actions = {
  setClient(store, name) {
    if (!name) {
      store.commit('clear')
    } else if (name !== store.state.name) {
      store.commit('set_name', name)
      store.dispatch('fetchContexts', name)
      store.dispatch('fetchTags', name)
    }
  },
  fetchContexts(store, client) {
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
  fetchTags(store, client) {
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
}

export default {
  namespaced: true,
  state () {
    return {
      name: '',
      contexts: [],
      tags: []
    }
  },
  mutations,
  actions
}