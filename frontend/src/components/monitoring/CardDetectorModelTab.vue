<template>

<div class="columns">

  <div class="column is-6">
    Click a node to view details 
    <GraphDataProvider :nodes="model">
      <LayeredGraphChart slot-scope="{chartNodes, chartEdges}" 
        :nodes="chartNodes" 
        :edges="chartEdges" 
        :centered="true"
        :selectable="true"
        :uniqueSelect="true"
        @selected="selected = $event"/>
    </GraphDataProvider>
  </div>

  <div v-if="selectedNode" class="column is-6 node-info">
    <div v-if="nodeIsInput">
      <div class="mb-1">
        <span class="has-text-grey-light has-text-weight-semibold">Client:</span> 
        <span>{{analysisDetails.client}}</span>
      </div>
      <div class="mb-1">
        <span class="has-text-grey-light has-text-weight-semibold">Tags:</span> 
        <b-taglist v-if="nodeDetails.tags.length > 0">
          <b-tag v-for="tag in nodeDetails.tags" :key="tag" class="has-background-grey-darker">{{tag}}</b-tag>
        </b-taglist>
        <span v-else>All</span>
      </div>
      <div class="mb-1">
        <span class="has-text-grey-light has-text-weight-semibold">Contexts:</span> 
        <b-taglist v-if="nodeDetails.contexts.length > 0">
          <b-tag v-for="context in nodeDetails.contexts" :key="context" class="has-background-grey-darker">{{context}}</b-tag>
        </b-taglist>
        <span v-else>All</span>
      </div>      
      <div>
        <span class="has-text-grey-light has-text-weight-semibold">Interval:</span>
        {{nodeDetails.interval}}
      </div>     
    </div>

    <template v-else>
      <div class="has-text-grey-lighter has-text-weight-semibold">Description</div>
      <div class="ml-4 mb-1">{{nodeDetails.desc}}</div>
      <div class="has-text-grey-lighter has-text-weight-semibold">Parameters</div>
      <div v-for="param in Object.keys(nodeDetails.paramsData)" :key="param" class="ml-4">
        <span> <b>{{param}}:</b> {{nodeDetails.paramsData[param]}} </span>
      </div>
     
    </template>  

  </div>


</div>

</template>


<script>
import GraphDataProvider from '@/components/detectionModel/GraphDataProvider'
import LayeredGraphChart from '@/components/detectionModel/LayeredGraphChart'

export default {
  components: {  GraphDataProvider, LayeredGraphChart },
  props: {
    analysisDetails: {
      type: Object,
      default: () => {return {}}
    },   
  },
  data() {
    return {
      selected: []      
    }
  },
  computed: {
    model() {
      return this.analysisDetails.hasOwnProperty('model') ? this.analysisDetails.model : []
    },
    inputOptions() {
      return this.analysisDetails.hasOwnProperty('data_options') ? this.analysisDetails.data_options : []
    },
    selectedNode() {
      return (this.selected.length > 0) ? this.model.find(elem => elem.id == this.selected[0]) : null
    },
    nodeIsInput() {
      return this.selectedNode.type === 'input'
    },
    nodeDetails() {
      if (this.nodeIsInput) {
        return this.inputOptions[parseInt(this.selectedNode.id)-1]
      } else {
        return this.model.find(elem => elem.id == this.selectedNode.id)
      }
    }

  },
  methods: {
       
  }

}
</script>

<style>
.node-info {
  border-left: 1px solid rgba(255,255,255,0.1);
}
</style>