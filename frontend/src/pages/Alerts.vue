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
      <div class="column  is-4">
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
  </div>

  <LayeredGraphChart :nodes="graphNodes" :edges="graphEdges"/>
</div>
</template>

<script>
import LayeredGraphChart from "../components/LayeredGraphChart"
import PipeNodeList from "../components/PipeNodeList"

import {nanoid} from 'nanoid'

export default {
  components: { LayeredGraphChart, PipeNodeList },
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
      graphEdges: []
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
          ...options,
        })
      }
      this.buildDirectedGraph()

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
      this.buildDirectedGraph()
    },
    buildDirectedGraph() {
      this.graphNodes = this.nodes.map(elem => ({id: elem.id, label: elem.title + ' (' + elem.id + ')'}))
      this.graphNodes.push({id: 'start', label: "Input data"})

      let edges = []
      this.nodes.forEach(elem => {
        if ((!elem.sourceNodes || elem.sourceNodes.length == 0) 
        && (elem.type === 'transformer' || elem.type === 'detector' )){
          edges.push({ source: 'start', target: elem.id})
        } else {
          if (elem.sourceNodes) {
            elem.sourceNodes.forEach(source => {
              edges.push({source: source.id, target: elem.id})
            })
          }         
        }
      })
      this.graphEdges = edges

    }
  }

};
</script>


<style scoped>

.column {
  border: 2px solid;
}

</style>