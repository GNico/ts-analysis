<template>

<div>
  <b-dropdown
    v-model="selectedNodes"
    multiple
    aria-role="list">
    <template #trigger>
      <b-tag
        class="button is-outlined"
        size="is-small"             
        icon-right="menu-down">
        Select nodes
        <b-icon size="is-small" icon="menu-down"/>
      </b-tag>
    </template>

    <b-dropdown-item v-for="item in model.nodes" :key="item.id" :value="item" aria-role="listitem">
      <span>{{item.type}} (ID: {{item.id}})</span>
    </b-dropdown-item>
  </b-dropdown>


  <b-taglist>
    <b-tag type="is-info" v-for="node in selectedNodes" :key="node.id">  {{node.type}} Id:{{node.id}}</b-tag>
  </b-taglist>

  <b-button @click="getNodesResults">
    Inspect selected
  </b-button>

  <div v-if="error">
    {{error}}
  </div>

  <div v-else>
    <div v-for="item in Object.keys(results)">
      <DebugNodeResult :series="results[item]['series']" :anomalies="addIdToAnomalies(results[item]['anomalies'])"/>
    </div>
  </div>
</div>
</template>


<script>

import api from "../../api/repository";
import DebugNodeResult from "./DebugNodeResult"
import {nanoid} from "nanoid"

export default {
  components: { DebugNodeResult },
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
      return this.activeResults.model
    },
    loadingResults() {
      return this.activeResults.loading
    },
    selectedNodesIds() {
      return this.selectedNodes.map(item => item.id)
    }
  },
  methods: {
    getNodesResults() {
      api.getResults(this.activeResults.taskId, {nodes: this.selectedNodesIds})
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



