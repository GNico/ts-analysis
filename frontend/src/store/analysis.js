import api from "../api/repository";

const state = {
  series: {},
  current: '',
}



const actions = {
	analizeSeries(store, options) {
        let requested = state.series[options.name]
        return  api.getAnomalies({
                    name: requested.client,
                    tags: requested.tags,
                    contexts: requested.contexts,
                    start: state.range.start,
                    end: state.range.end,
                    interval: options.interval,
                    config: options.config
                })
                .then(response => {       
                    store.commit('add_anomalies', response.data) 
                })
                .catch(error => { 
                    console.log('error retrieving anomalies')
                })
    }

}