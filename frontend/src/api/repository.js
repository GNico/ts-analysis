import axios from "axios";
import { nanoid } from 'nanoid';

const baseDomain = "http://localhost:8000";
const baseURL = baseDomain + "/ts_project";

const repository = axios.create({
    baseURL
})

const removeEmpty = obj => {
  Object.keys(obj).forEach((key) => (obj[key] == null || obj[key] == '') && delete obj[key]);
  return obj;
}

//change URL array params format (e.g. tags[] for tags)
const transformArrayParams = (params) => {
  const keys = Object.keys(params)
  let options = ''
  keys.forEach((key) => {
    const isParamTypeObject = typeof params[key] === 'object';
    const isParamTypeArray = isParamTypeObject && (params[key].length >= 0)   
    if (!isParamTypeObject ) {
      options += `${key}=${params[key]}&`
    }
    if (isParamTypeObject && isParamTypeArray) {      
      params[key].forEach((element) => {
        options += `${key}=${element}&`
      })
    }
  })
  return options ? options.slice(0, -1) : options;
}

export default {
    //Clients
    getClients() {
        return repository.get("/clients/")
    },
    getDataSourceNames() {
        return repository.get("/source-files/")
    },
    addNewClient(form) {
        return repository.post("/clients/", form)
    },
    deleteClient(clientName) {
        let url = "/clients/" + clientName + "/"
        return repository.delete(url)
    },
    getClientDetails(clientName) {
        let url = "/clients/" + clientName + "/"
        return repository.get(url)
    },

    //Series
    getSeriesData(params) {
        let url = "/clients/" + params.name + "/series/"
        delete params.name
        return repository.get(url, {params: removeEmpty(params), paramsSerializer: params => transformArrayParams(params)})
    },
    getTagsCount(params) {
        let url = "/clients/" + params.name + "/series/tagcount/"
        return repository.get(url, {params: removeEmpty(params), paramsSerializer: params => transformArrayParams(params)})
    },
    getContexts(clientName) {
        let url = "/clients/" + clientName + "/series/contexts/"
        return repository.get(url)
    },
    getTags(clientName) {
        let url = "/clients/" + clientName + "/series/tags/"
        return repository.get(url)
    },

    //Models
    getDetectionModels() {
        return repository.get("/pipelines/")
    },
    getPipelineTypes() {
        return repository.get("/nodes/")
    },
    addNewModel(model) {
        delete model.id
        return repository.post("/pipelines/", model)
    },
    updateModel(model) {
        const id = model.id
        delete model.id
        return repository.put("/pipelines/"+ id + "/", model)
    },
    deleteModel(id) {
        return repository.delete("/pipelines/" + id + "/")
    },

    //Running analysis & getting results
    getAnomalies(payload) {
        return repository.post("/analysis/", payload)
    },
    getResults(id, params) {
        console.log(params)
        if (!params) params = {}
        return repository.get("/analysis/" + id + "/", {
            params: removeEmpty(params),
            paramsSerializer: params => transformArrayParams(params),
            transformResponse: [
                ...axios.defaults.transformResponse,
                (data) => {      
                    if (!data.hasOwnProperty('result')) return data
                    var anoms = []
                    if (data.result.hasOwnProperty('anomalies')) {
                        for (var item of data.result.anomalies) {
                            anoms.push({
                                id: nanoid(8),
                                ...item
                            })
                        }
                    }
                    data.result.anomalies = anoms
                    return data                    
                }
            ]
        })
    },

    //Analysis settings
    getAllAnalysis() {
        return repository.get("/analysis-settings/")
    },
    getAnalysisDetails(id) {
        return repository.get("/analysis-settings/"+ id + "/", {
            transformResponse: [
                ...axios.defaults.transformResponse, 
                (data) => {
                    let formatted = {}
                    formatted.saveId = data.id
                    formatted.client = data.data_options.client
                    formatted.tags = data.data_options.tags
                    formatted.contexts = data.data_options.contexts
                    formatted.interval = data.data_options.interval
                    formatted.name = data.name
                    formatted.description = data.description
                    formatted.model = data.model
                    return formatted
                },
            ]
        })
    },
    addNewAnalysis(analysis) {
        return repository.post("/analysis-settings/", analysis)
    },
    updateAnalysis(analysis, id) {
        return repository.put("/analysis-settings/" + id + "/", analysis)
    },
    deleteAnalysis(id) {
        return repository.delete("/analysis-settings/" + id + "/")
    },
    deleteAnalysisList(ids) {
        return repository.delete("/analysis-settings/", { data: { ids: ids } })
    },


    //Misc
    testAlgo(testSource) {
        return repository.get("/testalgo?source=" + testSource)
    }
}
