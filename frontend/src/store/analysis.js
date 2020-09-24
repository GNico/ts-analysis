import api from "../api/repository";



//returns color from a tricolor gradient according to a 0 to 1 value
function getColorByvalue(value) {
    let color1 = ''
    let color2 = ''
    if (value<0.5) {
    value = value*2
    color1 = 'e4e814' //center - yellow
    color2 = '00ff00' //left - green
    } else {
    value = (value-0.5)*2
    color1 = 'db1313'  //right - red
    color2 = 'e4e814' //center - yellow
    }
    var hex = function(x) {
      x = x.toString(16);
      return (x.length == 1) ? '0' + x : x;
    };
    var r = Math.ceil(parseInt(color1.substring(0,2), 16) * value + parseInt(color2.substring(0,2), 16) * (1-value));
    var g = Math.ceil(parseInt(color1.substring(2,4), 16) * value + parseInt(color2.substring(2,4), 16) * (1-value));
    var b = Math.ceil(parseInt(color1.substring(4,6), 16) * value + parseInt(color2.substring(4,6), 16) * (1-value));
    return  '#' + (hex(r) + hex(g) + hex(b));
}

const state = {
  settings: {},
  results: {
    series: [],
    anomalies: [],
    baseline: [],
    trend: []
  },
  activeAnomalyId: '',
  loading: false,
}

const getters = {

    getAnomalies: (state) => {
        if ((state.results.hasOwnProperty('anomalies') 
        && Array.isArray(state.results.anomalies) 
        && state.results.anomalies.length)) {
            return state.results.anomalies
        } else {
            return []
        }
    },
    getAnomalyById: (state) => (id) => {
        if ((state.results.hasOwnProperty('anomalies') 
        && Array.isArray(state.results.anomalies) 
        && state.results.anomalies.length)) {
            return state.results.anomalies.find(item => item.id === id)
        }
    }

}

const mutations = {
    add_results(state, results) {
        state.results = { ...results }

        //add an id and color to each anomaly for UI purposes
        var anoms = []
        var idx = 0
        for (var item of results.anomalies) {
            anoms.push({
                    id: idx,
                    from: item.from,
                    to: item.to,
                    color: getColorByvalue(item.score/100),
                    score: item.score,
                })
            idx++
        }
        state.results.anomalies = anoms
    },
    set_active_anomaly(state, anomalyId) {
        state.activeAnomalyId = anomalyId
    }
}

const actions = {
	analizeSeries(store, settings) {
       return  api.getAnomalies({
                    name: settings.client,
                    tags: settings.tags,
                    contexts: settings.contexts,
                    //start: seriesOpts.start,
                    //end: seriesOpts.end,
                    interval: settings.interval,
                    //config: seriesOpts.config
                })
                .then(response => {       
                    store.commit('add_results', response.data) 
                })
                .catch(error => { 
                    console.log('error retrieving analysis')
                }) 
    },
    setActiveAnomaly(store, id) {
        store.commit('set_active_anomaly', id)
    },
}


export default {
    namespaced: true,
    getters,
    state,
    mutations,
    actions,
}