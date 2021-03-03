<template>
<div>
  <div>
    <div>Click to select the nodes you wish to inspect</div>
    <div><b-icon icon="information-outline" size="is-small"/> Order of selection corresponds to the order of results</div>
    <GraphDataProvider :nodes="model">
      <LayeredGraphChart 
        slot-scope="{chartNodes, chartEdges}" 
        :nodes="chartNodes" 
        :edges="chartEdges" 
        id="model" 
        :selectable="true" 
        :centered="false" 
        @selected="selectedNodes = $event"/>
    </GraphDataProvider>
    <b-button type="is-primary" label="Inspect selected" @click="getNodesResults"> </b-button>
  </div>


  <div v-if="error" class="item-section">
    {{error}}
  </div>

  <div v-else>
    <div v-for="item in Object.keys(formattedResults)">
      <DebugNodeResult 
        class="item-section" 
        :series="formattedResults[item]['series']" 
        :anomalies="formattedResults[item]['anomalies']"
        @updateRange="updateRange"
        :extremes="extremes"
        :node="getNode(item)">       
      </DebugNodeResult>
    </div>
  </div>
</div>
</template>


<script>

import api from "../../api/repository";
import DebugNodeResult from "./DebugNodeResult"
import GraphDataProvider from "../detectionModel/GraphDataProvider"
import LayeredGraphChart from "../detectionModel/LayeredGraphChart"
import {nanoid} from "nanoid"

export default {
  components: { DebugNodeResult, GraphDataProvider, LayeredGraphChart },
  data() {
    return {
      selectedNodes: [],
      selectedNodesOrder: [],
      results: {},
      error: '',
      extremes: {},
    }
  },
  computed: {
    activeResults() {
      return this.$store.getters['results/activeResults']
    },    
    model() {
      return this.activeResults.model
    },
    loadingResults() {
      return this.activeResults.loading
    },   
    formattedSelectedNodes() {
      let filtered = this.selectedNodes.filter(item => { return (item !== 'start' && item !== 'end')})
      if (filtered.length != this.selectedNodes.length) {
        filtered.push("_Root")
      }
      return filtered
    },
    formattedResults() {
      let formatted = {}
      this.selectedNodesOrder.forEach(nodeId => {
        if (nodeId === 'start') {
          if (this.results.hasOwnProperty("_Root")) {
            let startNode = { series: this.results["_Root"].series }
            formatted[nodeId] = startNode
          }
        } else if (nodeId === 'end') {
          if (this.results.hasOwnProperty("_Root")) {
            formatted[nodeId] = this.results["_Root"]
          }
        } else if (this.results.hasOwnProperty(nodeId)) {
          formatted[nodeId] = this.results[nodeId]
        }
      })
      return formatted
    }

  },
  methods: {
    getNodesResults() {
      this.selectedNodesOrder = [ ...this.selectedNodes ]
      if (!this.formattedSelectedNodes.length) {
        this.results = {}
        return
      }
      api.getResults(this.activeResults.taskId, {nodes: this.formattedSelectedNodes})
      .then(response => {
        this.results = response.data.node_results
        this.error = ''

        Object.keys(this.results).forEach(elem => {
          if (this.results[elem].hasOwnProperty('anomalies')) {
            this.results[elem].anomalies = this.addIdToAnomalies(this.results[elem].anomalies)
          }
        })
      })
      .catch(error => {
        if (error.response) {
          this.error = "There was an error fetching the results"
        } else if (error.request) {
          this.error = "The server could not be reached"
        } else {
          this.error = "Internal application error"
        }
      })
    },
    getNode(id) {
      if (id === 'start') return { display: 'Input data'}
      if (id === 'end') return {display: 'Result'}
      return this.model.find(item => item.id == id)
    },
    addIdToAnomalies(anomalies) {
      var anoms = []
      for (var item of anomalies) {
        anoms.push({
          id: nanoid(8),
          ...item
        })
      }
      return anoms                    
    },
    updateRange(newRange) {
      this.extremes = newRange
    }
  },
  created() {
  },
  mounted() {
  }
}

</script>

<style>
.item-section {
  margin-top: 2rem;
  margin-bottom: 2rem;
  border-top: 1px solid rgba(255,255,255,0.1);
}

</style>

