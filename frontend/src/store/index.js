import Vuex from 'vuex'
import Vue from 'vue'
import series from './series'
import clients from './clients'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    series,
    clients,
  }
})