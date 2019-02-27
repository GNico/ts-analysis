

const state = {
  series: {},
  default: {
    client: '',
    contexts: '',
    tags: '',
  }

}


const getters = {
    getSeriesNames: (state) => {
        return Object.keys(state.series)
    },
    getSeriesOptions: (state) => (name) => {
        if (!(name in state.series) ) {
            return state.default
        }
        else {
            return state.series[name]
        }
    }
}


const mutations = {
    add_series(state, payload) {
        state.series = { ...state.series, ...payload }
    },
    update_series(state, payload) {
        let { name, ...rest} = payload
        state.series[name] = { ...state.series[name], ...rest }
    },
    delete_series(state, payload) {
        let { [payload]:name, ...rest} = state.series
        state.series = rest 
    },

}

const actions = {
    addSeries(store, seriesOptions) {
        let { name, ...rest} = seriesOptions
        let newseries = { [name]: rest }
        store.commit("add_series", newseries)
        //add series in other modules
        store.dispatch('analysis/addSeries', name, { root: true })
    },
    deleteSeries(store, name) {
        store.commit("delete_series", name)
        //propagate deletes in other modules
        store.dispatch('analysis/deleteSeries', name, { root: true })

    },
    updateSeries(store, seriesOptions) {
        store.commit("update_series", seriesOptions)
        //propagate updates in other modules
        store.dispatch('analysis/fetchData', seriesOptions.name, { root: true })

    },
}

export default {
    namespaced: true,
    state,
    getters,
    mutations,
    actions
}