import api from "../api/repository";

const state = {
    all: [],
    nodeTypes: [],

}

const mutations = {
    set_models(state, models) {
      state.all = models
    },
    add_model(state, model) {
      state.all.push(model)
    },
    set_node_types(state, types) {
        state.nodeTypes = types
    },
}


const actions = {
    fetchModels(store) {
      return  api.getDetectionModels()
              .then(response => {       
                store.commit('set_models', response.data) 
              })
              .catch(error => { 
                console.log('error loading models')
                console.log(error)
              })  
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
    saveModel({store, dispatch},  model) {
      const apiCall =  model.id ? api.updateModel : api.addNewModel
      return  apiCall(model)
              .then(response => {
                dispatch('fetchModels')
              })
              .catch(error => { 
                console.log('error saving new model')
                console.log(error)
              })
    },
    deleteModel({store, dispatch}, id) {
      return  api.deleteModel(id)
              .then(response => {
                dispatch('fetchModels')
              })
    }

}


export default {
  namespaced: true,
  state,
  actions,
  mutations
}