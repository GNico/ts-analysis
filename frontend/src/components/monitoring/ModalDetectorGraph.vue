<template>

<ModalCard 
  :isActive="isActive" 
  @close="close"
  :title="title">

  <div>
    Click a node to view details 
    <GraphDataProvider :nodes="model">
      <LayeredGraphChart slot-scope="{chartNodes, chartEdges}" 
        :nodes="chartNodes" 
        :edges="chartEdges" 
        :centered="false"
        :selectable="true"
        :uniqueSelect="true"
        @selected="selected = $event"/>
    </GraphDataProvider>
  </div>

  <div v-if="selectedNode" >
    <div v-if="nodeIsInput">
      <div class="mb-1">
        <span class="has-text-grey-lighter has-text-weight-semibold">Tags:</span> 
        <b-taglist v-if="nodeDetails.tags.length > 0">
          <b-tag v-for="tag in nodeDetails.tags" :key="tag" class="has-background-grey-darker">{{tag}}</b-tag>
        </b-taglist>
        <span v-else>All</span>
      </div>
      <div class="mb-1">
        <span class="has-text-grey-lighter has-text-weight-semibold">Contexts:</span> 
        <b-taglist v-if="nodeDetails.contexts.length > 0">
          <b-tag v-for="context in nodeDetails.contexts" :key="context" class="has-background-grey-darker">{{context}}</b-tag>
        </b-taglist>
        <span v-else>All</span>
      </div>      
      <div>
        <span class="has-text-grey-lighter has-text-weight-semibold">Interval:</span>
        {{nodeDetails.interval}}
      </div>     
    </div>

    <div v-else>
      <div class="has-text-grey-lighter has-text-weight-semibold">Description</div>
      <div class="ml-4 mb-1">{{nodeDetails.desc}}</div>
      <div class="has-text-grey-lighter has-text-weight-semibold">Parameters</div>
      <div v-for="param in Object.keys(nodeDetails.paramsData)" :key="param" class="ml-4">
        <span> <b>{{param}}:</b> {{nodeDetails.paramsData[param]}} </span>
      </div>
     
    </div>  

  </div>


  <template v-slot:footer-right>
    <div>
      <button class="button is-small" @click="close">Close</button>
    </div>
  </template>

</ModalCard>


</template>


<script>
import ModalCard from '@/components/ModalCard'
import GraphDataProvider from '@/components/detectionModel/GraphDataProvider'
import LayeredGraphChart from '@/components/detectionModel/LayeredGraphChart'

export default {
  components: { ModalCard, GraphDataProvider, LayeredGraphChart },
  props: {
    analysisDetails: {
      type: Object,
      default: () => {return {}}
    },
    isActive: {
      type: Boolean,
      default: false
    },
    title: {
      type: String,
      default: 'Detection model'
    },
    minheight: {
      type: String,
      default: '',
    },   
    minwidth: {
      type: String,
      default: '',
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
    close() {
      this.$emit('close')
    },      
  }

}
</script>