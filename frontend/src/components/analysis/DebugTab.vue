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
    <b-tag type="is-info" v-for="node in selectedNodes">  {{node.type}} Id:{{node.id}}</b-tag>
  </b-taglist>

  <b-button @click="getNodesResults">
    Inspect selected
  </b-button>


  <div>
    {{results}}
  </div>

  <div>
    {{error}}
  </div>

</div>

</template>



<script>
import api from "../../api/repository";

export default {

  data() {
    return {
      selectedNodes: [],
      results: undefined,
      error: undefined,
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
      .then(response => this.results = response.data)
      .catch(error => this.error = error)
    }
  },
  created() {
  },
  mounted() {
  }
}

</script>



