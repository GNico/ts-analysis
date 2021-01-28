import axios from "axios";

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
    getClients() {
        return repository.get("/clients/")
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
    getAnomalies(payload) {
        return repository.get("/analysis/", {params: payload, paramsSerializer: params => transformArrayParams(params)})
    },
    getPipelineTypes() {
        return repository.get("/node-types/")
    },
    getDetectionModels() {
        return repository.get("/pipelines/")
    },
    addNewModel(model) {
        return repository.post("/pipelines/", model)
    },
    
    getAnalysis() {
        return repository.get("/analysis-settings/")
    },




    testAlgo(testSource) {
        return repository.get("/testalgo?source=" + testSource)
    }

}
