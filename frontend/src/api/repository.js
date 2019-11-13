import axios from "axios";

const baseDomain = "http://localhost:8000";
const baseURL = baseDomain + "/prueba";

const repository = axios.create({
    baseURL
})


export default {
    getClients() {
        return repository.get("/clients")
    },

    getContexts(clientName) {
        return repository.get("/contexts", {params: {name: clientName}})
    },

    getTags(clientName) {
        return repository.get("/tags", {params: {name: clientName}})
    },

    getSeriesData(payload) {
        return repository.get("/series", {params: payload})
    },

    getAnomalies(payload) {
        return repository.get("/anomalies", {params: payload})
    },

    addNewClient(payload) {
        return repository.post("/newclient", payload)
    },

    //remove later
    testAlgo(payload) {
        return repository.get("/testalgo", {params: payload} )
    }

}
