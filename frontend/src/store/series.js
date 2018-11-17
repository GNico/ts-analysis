const state = {
  clients: [
	  {
	    'name': 'Movistar',
	    'context': ['Facebook', 'Twitter', 'Instagram'],
	    'count': 2170000,
	    'start_date': '2/10/2017',
	    'end_date': '28/2/2018'
	  },
	  {
	    'name': 'Fravega',
	    'context': ['Twitter', 'Facebook', 'Webpage'],
	    'count': 500000,
	    'start_date': '3/11/2017',
	    'end_date': '1/3/2018'
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
	update_clients(state, payload) {
		state.clients = payload
	},
	add_data(state, payload) {
		state.data = payload
	},
	add_tags(state, payload) {
		state.tags = payload
	},
	update_range(state, payload) {
		state.range = payload
	}
}

//hosturl = 'http://localhost:8000/prueba/'

const actions = {
	fetchClients(store) {
		return axios.get('http://localhost:8000/prueba/clients/')
		.then(response => {       
	      store.commit('update_clients', response.data) 

	    })
	    .catch(error => { 
	      console.log('error loading client data')
	    })
	},
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
	      console.log('error loading series data')
	    })
	},
	fetchTags(store) {
		return axios.get('http://localhost:8000/prueba/tags/')
        .then(response => {
	      store.commit('add_tags', response.data) 
        })
        .catch(error => { 
            console.log('error loading tag data');
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