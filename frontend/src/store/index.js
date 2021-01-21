import Vuex from 'vuex'
import Vue from 'vue'
import series from './series'
import visualize from './visualize'
import analysis from './analysis'
import clients from './clients'
import models from './models'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
  	series,
    visualize,
    analysis,
    clients,
    models,
  }
})