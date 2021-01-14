<template>

<div>
  <div class="columns">    
    <div class="column is-offset-1 is-3">
      <PipeNodeList 
        title="Transformers" 
        type="transformer"
        :nodeSpecs="nodeSpecs" 
        :nodes="nodes" 
        @newNode="createNode"
        @nodeParamsUpdate="updateNodeParams"
        @nodeInputUpdate="updateNodeInputs"/>
    </div>
    <div class="column is-offset-1 is-3">
      <PipeNodeList 
        title="Detectors" 
        type="detector"
        :nodeSpecs="nodeSpecs" 
        :nodes="nodes" 
        @newNode="createNode"/>
    </div>
    <div class="column is-offset-1 is-3">
      <PipeNodeList 
        title="Aggregators" 
        type="aggregator"
        :nodeSpecs="nodeSpecs" 
        :nodes="nodes" 
        @newNode="createNode"/>
    </div>
  </div>

  <LayeredGraphChart/>
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
      ]
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
    updateNodeInputs(event) {
      //nothing
    }
  }

};
</script>


<style>

</style>