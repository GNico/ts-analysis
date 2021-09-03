import Vuex from 'vuex'
import Vue from 'vue'
import visualize from './visualize'
import analysis from './analysis'
import results from './results'
import clients from './clients'
import models from './models'
import { getValidUserUTCOffset } from '@/utils/datetimeConstants'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    UTCOffset: getValidUserUTCOffset(),
  },
  mutations: {
    set_utcoffset(state, value) {
      state.UTCOffset = value
    }
  },
  modules: {
    visualize,
    analysis,
    results,
    clients,
    models,
  }
})