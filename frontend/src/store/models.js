import api from "../api/repository";

const state = {
    all: [],
    nodeTypes: [],

}

const mutations = {

    set_node_types(state, types) {
        state.nodeTypes = types
    }
}


const actions = {
    fetchModels(store) {
       /* return  api.getPipelineTypes()
                .then(response => {       
                  store.commit('set_node_specs', response.data) 
                })
                .catch(error => { 
                  console.log('error loading pipeline types')
                  console.log(error)
                })  */
    },
    fetchNodeTypes(store) {
        return  api.getPipelineTypes()
                .then(response => {       
                  store.commit('set_node_types', response.data) 
                })
                .catch(error => { 
                  console.log('error loading pipeline types')
                  console.log(error)
                }) 
    },
    addModel(store, model) {

    },
    deleteModel(store, id) {

    }

}


export default {
  namespaced: true,
  state,
  actions,
  mutations
}