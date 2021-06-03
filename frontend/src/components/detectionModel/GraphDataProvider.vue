<script>
import { validate } from './ModelValidation'
  
export default {
  props: { 
    nodes: {
      type: Array,
      default: () => []
    },
  },
  data() {
    return {
    }
  },
  computed: {
    bidirectionalNodes() {
      let graphNodes = {}
      this.nodes.forEach(elem => {
        graphNodes[elem.id] = {id: elem.id, display: elem.display, group: elem.group, type: elem.type, source: elem.sources, target: []}
      })
      //add in and out edges to each node
      Object.keys(graphNodes).forEach(id => {
        let sourceIds = []
        graphNodes[id].source.forEach(sourceElem => {
          sourceIds.push(sourceElem)
          graphNodes[sourceElem].target.push(id)
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
          label: elem.display + ' (' + elem.id + ')'
        })
      })
      //start and end nodes
      if (nodes.length > 0) {
       // nodes.push({id: 'start', label: 'Input data'})
        nodes.push({id: 'end', label: 'Result'})
      }
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
            console.log("nothing")
           // edges.push({source: 'start', target: elem.id})
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
    bidirectionalNodes: {
      immediate: true,
      handler(newVal) {
        let validationMessages = validate(newVal)
        this.$emit('validation', validationMessages)
      }      
    },
  },
  render() {
    return this.$scopedSlots.default({
      chartNodes: this.chartNodes,
      chartEdges: this.chartEdges
    })
  }
}

</script>