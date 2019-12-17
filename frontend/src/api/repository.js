import axios from "axios";

const baseDomain = "http://localhost:8000";
const baseURL = baseDomain + "/prueba";

const repository = axios.create({
    baseURL
})

const removeEmpty = obj => {
  Object.keys(obj).forEach((key) => (obj[key] == null || obj[key] == '') && delete obj[key]);
  return obj;
}

export default {
    getClients() {
        return repository.get("/clients/")
    },
    addNewClient(form) {
        return repository.post("/clients/", form)
    },
    getSeriesData(params) {
        let url = "/clients/" + params.name + "/series/"
        delete params.name
        return repository.get(url, {params: removeEmpty(params)})
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
        return repository.get("/anomalies/", {params: payload})
    },
    //remove later
    testAlgo(payload) {
        return repository.get("/testalgo/", {params: payload} )
    }

}
