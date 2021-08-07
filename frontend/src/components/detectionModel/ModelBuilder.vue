<template>
<div>  
  <div class="columns bordered-columns">    
    <div class="column is-5 is-paddingless">
      <div class="p-3 bordered-column has-background-grey-dark" v-for="group in groups" :key="group">
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

    <div class="column">
      <div class="buttons is-flex is-justify-content-flex-end">
        <b-button 
          type="is-info"
          size="is-small"
          icon-left="plus"
          @click="addInput">
          Add Input Node
        </b-button>
        <b-button 
          type="is-info"
          size="is-small"
          icon-left="delete"
          :disabled="!inputNodes.length"
          @click="removeInput">
          Remove Input Node
        </b-button>
      </div>

      <GraphDataProvider :nodes="nodes" @validation="validationMessages = $event" >
        <LayeredGraphChart 
          ref="graph"
          slot-scope="{chartNodes, chartEdges}" 
          :nodes="chartNodes" 
          :edges="chartEdges" 
          centered
          :horizontal="false"
          selectable
          uniqueSelect
          :selected="sharedState.openNode ? [sharedState.openNode] : []"
          @selected="openNode"/>
      </GraphDataProvider>
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
</template>


<script>
import PipeNodeList from "./PipeNodeList"
import cloneDeep from "lodash/cloneDeep";
import GraphDataProvider from "./GraphDataProvider"
import LayeredGraphChart from "./LayeredGraphChart"
import { customAlphabet } from 'nanoid'

const nanoid = customAlphabet('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQLRSTUVWXYZ', 3)

export default {
  components: { GraphDataProvider, PipeNodeList, LayeredGraphChart },
  props: {
    nodes: {
      type: Array,
      default: () => []
    }
  },
  inject: {
    sharedState: {
      name: 'sharedState',
      default: {}
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
    },    
    inputNodes() {
      return this.nodes.filter(elem => elem.group == "input")
    },
  },
  methods: {  
    openNode(selected) {
      this.sharedState.openNode = selected[0]
    }, 
    addInput() {
      let modelCopy = cloneDeep(this.nodes)
      let newNode = this.getNewInputNode()
      modelCopy.push(newNode)
      this.updateModel(modelCopy)
    },
    removeInput() {
      let inputNumber = this.inputNodes.length
      this.deleteNode(inputNumber.toString())
    },
    getNewInputNode() {
      let inputNumber = this.inputNodes.length + 1
      let newNode = {
        id: inputNumber.toString(),
        type: 'input',
        group: 'input',
        sources: [],
        debug: true,
        display: 'Input',
        desc: '',
      }
      return newNode
    },
    generateNewNodeId() {
      let newid = nanoid()
      let found = true
      while (found) {
        found = this.nodes.some(el => el.id === newid)
        if (found) {
          newid = nanoid()
        }
      }
      return newid
    },
    createNode({type, group}) {
      let modelCopy = cloneDeep(this.nodes)
      let definition = this.nodeTypes[group].find(elem => elem.type === type)
      if (definition) {
        let newNode = {
          id: this.generateNewNodeId(),
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
        //add an input if needed
        if (!this.inputNodes.length)
          modelCopy.push(this.getNewInputNode())
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
  },
  watch: {
    'sharedState.openNode'(newVal) {
      if (!newVal) this.$refs.graph.clearSelected()
    }
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
  border-top: 0;
}

.bordered-columns .bordered-column:first-child {
  border-top: 2px solid rgba(255,255,255,0.1);
}

</style>