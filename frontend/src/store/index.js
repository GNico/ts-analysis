import Vuex from 'vuex'
import Vue from 'vue'
import visualize from './visualize'
import analysis from './analysis'
import results from './results'
import clients from './clients'
import models from './models'


Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    visualize,
    analysis,
    results,
    clients,
    models,
  }
})