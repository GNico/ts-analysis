const state = {
  clients: [
	  {
	    'name': 'Personal',
	    'context': 'Twitter',
	  },
	  {
	    'name': 'Movistar',
	    'context': 'Facebook',
	}],
  data: [],
  tags: [],
  range: {
  	start: null,
  	end: null
  },
  loading: null
}

const namespaced = true

const mutations = {
	add_data(state, payload) {
		state.data = payload
	},
	add_tags(state, payload) {
		state.tags = payload
	},
	modify_range(state, payload) {
		state.range = payload
	}
}

//hosturl = 'http://localhost:8000/prueba/'

const actions = {
	fetchData(store) {
		// sets `state.loading` to true. Show a spinner or something.
	     console.log('data pending')

		return axios.get('http://localhost:8000/prueba/series/')
	    .then(response => {       
	      // sets `state.loading` to false 
	      // also sets `state.apiData to response`
	      store.commit('add_data', response.data) 

	    })
	    .catch(error => { 
	      // set `state.loading` to false and do something with error   
	      console.log('error')
	    })
	},
	fetchTags(store) {
		return axios.get('http://localhost:8000/prueba/tags/')
        .then(response => {
	      store.commit('add_tags', response.data) 
        })
        .catch(error => { 
            console.log(error);
        });
	},
	updateData(store) {
		//fetch new data based on currentclient and range
	}
}

export default {
  state,
  actions,
  mutations
}