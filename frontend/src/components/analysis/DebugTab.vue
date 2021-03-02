<template>
<div>
  <div>
    Click to select the nodes you wish to inspect
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
    <div v-for="item in Object.keys(results)">
      <DebugNodeResult 
        class="item-section" 
        :series="results[item]['series']" 
        :anomalies="addIdToAnomalies(results[item]['anomalies'])" 
        :node="item"/>
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
      results: {},
      error: '',
    }
  },
  computed: {
    activeResults() {
      return this.$store.getters['results/activeResults']
    },    
    model() {
      console.log("model changes somehow")
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
  },
  methods: {
    getNodesResults() {
      if (!this.formattedSelectedNodes.length) {
        this.results = {}
        return
      }
      api.getResults(this.activeResults.taskId, {nodes: this.formattedSelectedNodes})
      .then(response => {
        this.results = response.data.node_results
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
    getNode(id) {
      return this.model.find(item => item.id = id)
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

