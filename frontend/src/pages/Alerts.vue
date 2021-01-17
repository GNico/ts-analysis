<template>

<div>
  <div class="container section">
    <div class="columns has-background-grey-dark">    
      <div class="column is-4">
        <PipeNodeList 
          title="Transformers" 
          type="transformer"
          :nodeSpecs="nodeSpecs" 
          :nodes="nodes" 
          @newNode="createNode"
          @nodeParamsUpdate="updateNodeParams"
          @nodeSourceUpdate="updateNodeSource"/>
      </div>
      <div class="column is-4">
        <PipeNodeList 
          title="Detectors" 
          type="detector"
          :nodeSpecs="nodeSpecs" 
          :nodes="nodes" 
          @newNode="createNode"
          @nodeParamsUpdate="updateNodeParams"
          @nodeSourceUpdate="updateNodeSource"/>
      </div>
      <div class="column is-4">
        <PipeNodeList 
          title="Aggregators" 
          type="aggregator"
          :nodeSpecs="nodeSpecs" 
          :nodes="nodes" 
          @newNode="createNode"
          @nodeParamsUpdate="updateNodeParams"
          @nodeSourceUpdate="updateNodeSource"/>
      </div>
    </div>

    <div v-for="msg in validationMessages">  
      <span v-if="msg.type=='warning'" class="has-text-link">
        <b-icon icon="alert-circle" size="is-small"></b-icon>
         {{msg.message}} ({{msg.id}})
      </span>
      <span v-if="msg.type=='invalid'" class="has-text-warning">
        <b-icon icon="close-octagon" size="is-small"></b-icon>
        {{msg.message}}
      </span>
    </div>
  </div>

  <GraphBuilder :nodes="nodes" @validation="validationMessages = $event"/>
</div>
</template>

<script>
import GraphBuilder from "../components/detectionModel/GraphBuilder"
import PipeNodeList from "../components/detectionModel/PipeNodeList"

import {nanoid} from 'nanoid'


export default {
  components: { GraphBuilder, PipeNodeList },
  data() {
    return {
      nodes: [],
      nodeSpecs: [
        {
          title: 'Rolling window',
          desc: 'Some description',
          type: 'transformer',
          params: [
          {
            name: 'window',
            type: 'number',
          },
          {
            name: 'agg',
            type: 'string',        
          },
          {
            name: 'boolfield',
            type: 'boolean',        
          }]
        },
        {
          title: 'Double rolling window',
          desc: 'Some description',
          type: 'transformer',
          params: []
        },
        {
          title: 'Level shift detector',
          desc: 'Some description',
          type: 'detector',
          params: []
        },
        {
          title: 'Outlier detector',
          desc: 'Some description',
          type: 'detector',
          params: []
        },
        {
          title: 'OR Aggregator',
          desc: 'Some description',
          type: 'aggregator',
          params: []
        },
        {
          title: 'AND aggregator',
          desc: 'Some description',
          type: 'aggregator',
          params: []
        },
      ],
      graphNodes: [],
      graphEdges: [],
      validationMessages: [],
    }
  },
  computed: {


  },
  methods: {
    createNode(name) {
      let newid = nanoid(3)
      let found = true
      while (found) {
        found = this.nodes.some(el => el.id === newid)
        if (found) {
          newid = nanoid(3)
        }
      }
      let options = this.nodeSpecs.find(elem => elem.title === name)
      if (options) {
        this.nodes.push({
          id: newid,
          sourceNodes: [],
          ...options,
        })
      }
    },
    updateNodeParams(event) {
      let nodeIndex = this.nodes.findIndex(elem => elem.id === event.id)
      if (nodeIndex != -1) {
        let id, newParamsValues;
        ({ id, ...newParamsValues } = event )
        let nodeCopy = { ...this.nodes[nodeIndex]}
        nodeCopy.paramsData = { ...nodeCopy.paramsData, ...newParamsValues }
        this.nodes.splice(nodeIndex, 1, nodeCopy)
      }
    },
    updateNodeSource(event) {
      let nodeIndex = this.nodes.findIndex(elem => elem.id === event.id)
      if (nodeIndex != -1) {
        let nodeCopy = { ...this.nodes[nodeIndex]}
        nodeCopy.sourceNodes = event.sourceNodes
        this.nodes.splice(nodeIndex, 1, nodeCopy)
      } 
    },    
  }
};
</script>


<style scoped>

.column {
  border: 2px solid;
}

</style>