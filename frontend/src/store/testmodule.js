const mutations = {
	set_name(state, payload) {
        state.name = payload
    },
}

const actions = {
	changeName(store, name) {
		store.commit('set_name', name)
	}
}

export default {
  namespaced: true,
  state () {
    return {
      name: 'aname',
	  testdata: 'somedata',
    }
  },
  mutations,
  actions,
}