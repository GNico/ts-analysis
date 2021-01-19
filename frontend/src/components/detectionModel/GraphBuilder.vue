<template>
<div>
  <LayeredGraphChart id="model" :nodes="chartNodes" :edges="chartEdges"/>
</div>
</template>


<script>

import LayeredGraphChart from './LayeredGraphChart'
import { validate } from './ModelValidation'
  
export default {
  components: { LayeredGraphChart },
  props: { 
    nodes: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
    }
  },
  computed: {
    bidirectionalNodes() {
      let graphNodes = {}
      this.nodes.forEach(elem => {
        graphNodes[elem.id] = {id: elem.id, group: elem.group, type: elem.type, source: elem.sourceNodes, target: []}
      })
      //add in and out edges to each node
      Object.keys(graphNodes).forEach(id => {
        let sourceIds = []
        graphNodes[id].source.forEach(sourceElem => {
          sourceIds.push(sourceElem.id)
          graphNodes[sourceElem.id].target.push(id)
        })
        graphNodes[id].source = sourceIds
      })
      return graphNodes
    }, 
    chartNodes() {
      let nodes = []
      Object.keys(this.bidirectionalNodes).forEach(elemId => {
        let elem = this.bidirectionalNodes[elemId]
        nodes.push({
          id: elem.id,
          label: elem.type + ' (' + elem.id + ')'
        })
      })
      //start and end nodes
      nodes.push({id: 'start', label: 'Input data'})
      nodes.push({id: 'end', label: 'Result'})
      return nodes
    },
    chartEdges() {
      let edges = []
      Object.keys(this.bidirectionalNodes).forEach(elemId => {     
        let elem = this.bidirectionalNodes[elemId] 
        if (!elem.target || elem.target.length == 0) {
          if (elem.group == 'detector' || elem.group == 'aggregator') 
            edges.push({source: elem.id, target: 'end'})          
        }
        if (!elem.source || elem.source.length == 0) {
          if (elem.group == 'transformer' || elem.group == 'detector') 
            edges.push({source: 'start', target: elem.id})
        } else {
          elem.source.forEach(sourceId => {
            edges.push({source: sourceId, target: elem.id})
          })
        }
      })
      return edges
    }
  },

  watch: {
    bidirectionalNodes(newVal) {
      let validationMessages = validate(newVal)
      this.$emit('validation', validationMessages)
    }
  }


}

</script>