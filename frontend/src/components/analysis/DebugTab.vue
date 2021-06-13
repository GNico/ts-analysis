<template>
<div>
  <div>
    <div>Click to select the nodes you wish to inspect</div>
    <div><b-icon icon="information-outline" size="is-small"/> Order of selection corresponds to the order of results</div>
    <GraphDataProvider :nodes="model">
      <LayeredGraphChart 
        ref="graphChart"
        slot-scope="{chartNodes, chartEdges}" 
        :nodes="chartNodes"
        :edges="chartEdges" 
        :selectable="true" 
        :centered="false" 
        @selected="selectedNodes = $event"/>
    </GraphDataProvider>
    <b-button type="is-primary" label="Inspect selected" @click="getNodesResults" :disabled="!isSelected"> </b-button>
    <b-button type="is-primary" label="Clear all" @click="clearSelected" :disabled="!isSelected"> </b-button>
  </div>

  <div v-if="error" class="item-section">
    {{error}}
  </div>

  <div v-else>
    <div v-for="item in Object.keys(results)">
      <DebugNodeResult 
        class="item-section" 
        :series="results[item]['series']" 
        :anomalies="results[item]['anomalies']"
        @updateRange="updateRange"
        :extremes="extremes"
        :node="getNode(item)"/>       
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
  provide() {
    return {
      sharedState: this.sharedState
    }
  },
  data() {
    return {
      selectedNodes: [],
      selectedNodesOrder: [],
      results: {},
      error: '',
      extremes: {},
      sharedState: {
        crosshair: {}
      }
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
    isSelected() {
      return this.selectedNodes.length > 0
    }
  },
  methods: {
    getNodesResults() {
      this.selectedNodesOrder = [ ...this.selectedNodes ]
      if (!this.selectedNodes.length) {
        this.results = {}
        return
      }
      api.getResults(this.activeResults.taskId, {nodes: this.selectedNodes})
      .then(response => {
        this.results = this.formatResults(response.data.result)
        this.error = ''
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
    formatResults(result) {
      let formatted = {}
      this.selectedNodesOrder.forEach(nodeId => {       
        if (!isNaN(parseInt(nodeId))) { //numeric id = is input
          formatted[nodeId] = {
            series: {
              nodeId: result.series[nodeId]
            },
            anomalies: [],
          }
        } else if (nodeId === 'end') {
          formatted[nodeId] = { 
            series: result.series, 
            anomalies: this.addIdToAnomalies(result.anomalies)
          }
        } else if (result.debug_nodes[nodeId]) {
          formatted[nodeId] = { 
            series: result.debug_nodes[nodeId].series,
            anomalies: this.addIdToAnomalies(result.debug_nodes[nodeId].anomalies)
          }
        }
      })
      return formatted
    },
    getNode(id) {
      if (!isNaN(parseInt(id))) {
        return {display: 'Input ' + id}
      }
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
    },
    clearSelected() {
      this.$refs.graphChart.clearSelected()
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

