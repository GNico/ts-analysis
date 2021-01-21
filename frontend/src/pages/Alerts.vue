<template>
<div>
  <div class="container section">
    <div class="columns has-background-grey-dark">    
      <div class="column is-4" v-for="group in groups" :key="group">
        <PipeNodeList          
          :group="group"
          :nodeSpecs="nodeSpecs" 
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


    <GraphBuilder :nodes="nodes" @validation="validationMessages = $event"/>

  </div>

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
      groups: [ "transformer", "detector", "aggregator"],
      nodeSpecs: [
       /*   {
            group: "detector",
            type: "EMA",
            display: "Exponential moving average",
            desc: "Exponential moving average with decay rate and minimum required threshold",
            params: [
              {
                id: "decay",
                type: "BoundedFloat",
                display: "Decay",
                desc: "Decay rate",
                value: 0.9,
                min: 0,
                max: 1
              },
              {
                id: "threshold",
                type: "Float",
                display: "Deviations threshold",
                desc: "Min required deviations threshold",
                value: 2
              }
            ]
        }, */
        {
          type: 'Rolling window',
          desc: 'Some description',
          group: 'transformer',
          params: [
          {
            id: 'window',
            type: 'Float',
            display: 'Window',
            value: 2,
          },
          {
            id: 'decay',
            type: "BoundedFloat",
            display: "Decay",
            desc: "Decay rate",
            value: 0.9,
            min: 0,
            max: 1
          },
          {
            id: 'another field',
            type: 'boolean',        
          }]
        },
        {
          type: 'Level shift detector',
          desc: 'Some description',
          group: 'detector',
          params: []
        },
        {
          type: 'Outlier detector',
          desc: 'Some description',
          group: 'detector',
          params: []
        },
        {
          type: 'OR Aggregator',
          desc: 'Some description',
          group: 'aggregator',
          params: []
        },
        {
          type: 'AND aggregator',
          desc: 'Some description',
          group: 'aggregator',
          params: []
        },
      ],
      validationMessages: [],
    }
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
      let options = this.nodeSpecs.find(elem => elem.type === name)
      if (options) {
        let newNode = {
          id: newid,
          sourceNodes: [],
          ...options,
        }
        //fill default param values
        let paramsData = {}
        if (options.params && options.params.length > 0) {
          options.params.forEach(param => {
            if (param.hasOwnProperty('value')) {
              paramsData[param.id] = param.value
            }
          })
        }
        newNode['paramsData'] = paramsData
        this.nodes.push(newNode)
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
    deleteNode(id) {
      for (var i = this.nodes.length - 1; i >= 0; i--) {
        if (this.nodes[i].id === id) {
          this.nodes.splice(i, 1)
        } else {
          for (var j = this.nodes[i].sourceNodes.length - 1; j >= 0; j--) {
            if (this.nodes[i].sourceNodes[j].id === id) {
              this.nodes[i].sourceNodes.splice(j, 1)
            }
          }
        }
      }     
    }    
  }
};
</script>


<style scoped>

.column {
  border: 2px solid;
}

</style>