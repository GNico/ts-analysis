<template>
<div>
  <div class="columns bordered-columns has-background-grey-dark">    
    <div class="column is-4 bordered-column" v-for="group in groups" :key="group">
      <PipeNodeList          
        :group="group"
        :nodesDefinition="nodeTypes[group]" 
        :nodes="nodes" 
        @newNode="createNode"
        @nodeParamsUpdate="updateNodeParams"
        @nodeSourceUpdate="updateNodeSource"
        @nodeDelete="deleteNode"/>
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

  <GraphDataProvider :nodes="nodes" @validation="validationMessages = $event" >
    <LayeredGraphChart slot-scope="{chartNodes, chartEdges}" :nodes="chartNodes" :edges="chartEdges"/>
  </GraphDataProvider>
</div>
</template>


<script>
import PipeNodeList from "./PipeNodeList"
import cloneDeep from "lodash/cloneDeep";
import { customAlphabet } from 'nanoid'

import GraphDataProvider from "./GraphDataProvider"
import LayeredGraphChart from "./LayeredGraphChart"

const nanoid = customAlphabet('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQLRSTUVWXYZ', 3)

export default {
  components: { GraphDataProvider, PipeNodeList, LayeredGraphChart },
  props: {
    nodes: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      validationMessages: [],
    }
  },
  computed: {
    nodeTypes() {
      return this.$store.state.models.nodeTypes
    },
    groups() {
      return Object.keys(this.nodeTypes)
    }
  },
  methods: {
    createNode({type, group}) {
      let modelCopy = cloneDeep(this.nodes)
      let newid = nanoid()
      let found = true
      while (found) {
        found = this.nodes.some(el => el.id === newid)
        if (found) {
          newid = nanoid()
        }
      }
      let definition = this.nodeTypes[group].find(elem => elem.type === type)
      if (definition) {
        let newNode = {
          id: newid,
          type: type,
          group: group,
          sources: [],
          debug: true,
          display: definition.display,
          desc: definition.desc
        }
        //fill default param values
        let paramsData = {}
        if (definition.params && definition.params.length > 0) {
          definition.params.forEach(param => {
            if (param.hasOwnProperty('value')) {
              paramsData[param.id] = param.value
            }
          })
        }
        newNode['paramsData'] = paramsData
        modelCopy.push(newNode)
        this.updateModel(modelCopy)
      }
    },
    updateNodeParams(event) {
      let modelCopy = cloneDeep(this.nodes)
      let nodeIndex = modelCopy.findIndex(elem => elem.id === event.id)
      if (nodeIndex != -1) {
        let id, newParamsValues;
        ({ id, ...newParamsValues } = event )
        let nodeCopy = { ...modelCopy[nodeIndex]}
        nodeCopy.paramsData = { ...nodeCopy.paramsData, ...newParamsValues }
        modelCopy.splice(nodeIndex, 1, nodeCopy)
      }
      this.updateModel(modelCopy)
    },
    updateNodeSource(event) {
      let modelCopy = cloneDeep(this.nodes)
      let nodeIndex = modelCopy.findIndex(elem => elem.id === event.id)
      if (nodeIndex != -1) {
        let nodeCopy = { ...modelCopy[nodeIndex]}
        nodeCopy.sources = event.sources
        modelCopy.splice(nodeIndex, 1, nodeCopy)
      } 
      this.updateModel(modelCopy)
    },
    deleteNode(id) {
      let modelCopy = cloneDeep(this.nodes)
      for (var i = modelCopy.length - 1; i >= 0; i--) {
        console.log(modelCopy[i])
        if (modelCopy[i].id === id) {
          modelCopy.splice(i, 1)
        } else {
          for (var j = modelCopy[i].sources.length - 1; j >= 0; j--) {
            if (modelCopy[i].sources[j] === id) {
              modelCopy[i].sources.splice(j, 1)
            }
          }
        }
      }   
      this.updateModel(modelCopy)
    },
    updateModel(newModel) {
      this.$emit('input', newModel)
    },   
  }, 
  created() {
    this.$store.dispatch('models/fetchNodeTypes')          
  }
};
</script>


<style scoped>

.bordered-columns {
  margin-right: 0;
  margin-left: 0;
}

.bordered-columns .bordered-column {
  border: 2px solid rgba(255,255,255,0.1);
  border-left: 0;
}

.bordered-columns .bordered-column:first-child {
  border-left: 2px solid rgba(255,255,255,0.1);
}

</style>