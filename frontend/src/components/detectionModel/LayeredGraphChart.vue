<template>
<div ref="container">
  <svg> 
    <g/>
    <rect/>
  </svg>
</div>
</template>

<script>
import dagreD3 from 'dagre-d3'
import * as d3 from 'd3'
import { nanoid } from 'nanoid'
import debounce from 'lodash/debounce'
import isEqual from 'lodash/isEqual'
import sortBy from 'lodash/sortBy'

export default {
  props: {
    nodes: {
      type: Array,
      default: () => []
    },
    edges: {
      type: Array,
      default: () => []
    },
    selectable: {
      type: Boolean,
      default: false,
    },
    uniqueSelect: {
      type: Boolean,
      default: false,
    },
    centered: {
      type: Boolean,
      default: true,
    },
    horizontal: {
      type: Boolean,
      default: true
    },


    selected: {
      type: Array,
      default: () => []
    }


  },
  data() {
    return {
      id: '',
      resizeHandler: debounce(this.refresh, 300),
      g: undefined,   
      selectedNodes: [],    
    }
  },
  computed: {
    renamedNodes() {  //add prefix to nodes id to avoid ids starting with number
      var renamed = []
      this.nodes.forEach(node => {
        let nodeCopy = { ...node }
        nodeCopy.id = this.addIdPrefix(nodeCopy.id)
        renamed.push(nodeCopy)
      })
      return renamed
    },
    renamedSelected() {
      var renamed = []
      this.selected.forEach(id => {
        renamed.push(this.addIdPrefix(id))
      })
      return renamed
    },
    cursor() {
      return this.selectable ? 'cursor: pointer;' : ''
    },
  },
  methods: {
    addIdPrefix(id) {
      return "N" + this.id + id 
    },
    removeIdPrefix(id) {
      return id.substring(7);
    },
    createLayout() {
      this.g = new dagreD3.graphlib.Graph().setGraph({})
      if (this.horizontal) this.g.graph().rankDir = 'LR';
      // Add nodes
      this.renamedNodes.forEach((item, index) => {
        item.rx = item.ry = 5;
        this.g.setNode(item.id, item);
        if (this.selectedNodes.includes(item.id)) {
          this.g.node(item.id).style = 'fill: green; stroke: yellow;' + this.cursor
          this.g.node(item.id).labelStyle = 'fill:  yellow;' + this.cursor
        } else {
          this.g.node(item.id).style = 'fill:#005aff; stroke: white;' + this.cursor
          this.g.node(item.id).labelStyle = 'fill:  white;' + this.cursor
        }        
      });
      // Link relationship
      this.edges.forEach(item => {
        this.g.setEdge(this.addIdPrefix(item.source), this.addIdPrefix(item.target), {
          label: item.label,
          style: "stroke: lightblue; fill: none; stroke-width: 1px",
          arrowheadStyle: "fill: lightblue; stroke: lightblue;",
          arrowhead: 'vee',
        });
      });
    },
    toggleSelected(nodeId) {
      let index = this.selectedNodes.findIndex(elem => elem == nodeId)
      if (index === -1) {
        if (this.uniqueSelect) {
          this.clearSelected()
        }
        this.selectedNodes.push(nodeId)
        this.paintSelected(nodeId)
      } else {
        this.selectedNodes.splice(index, 1)
        this.paintUnselected(nodeId)
      }
    },
    clearSelected() {
      this.selectedNodes.forEach(elem => this.paintUnselected(elem))
      this.selectedNodes = []
    },
    paintSelected(nodeId) {
      d3.select("#" + nodeId + ' rect').attr('style', 'fill: green; stroke: yellow;' + this.cursor) 
      d3.select("#" + nodeId + ' text').attr('style', 'fill: yellow;' + this.cursor) 
    },
    paintUnselected(nodeId) {
      d3.select("#" + nodeId + ' rect').attr('style', 'fill: #005aff; stroke: white;' + this.cursor) 
      d3.select("#" + nodeId + ' text').attr('style', 'fill:  white;' + this.cursor)
    },
    drawChart() {
      //Draw graphics
      var container = this.$refs.container
      var svg = d3.select(container).select("svg")
      var inner = svg.select("g");
      var container = this.$refs.container
      var maxWidth = container.clientWidth
      svg.attr("width", maxWidth)      

      // Set up zoom support
      var zoom = d3.zoom().on("zoom", function () {
          inner.attr("transform", d3.event.transform);
      });
      svg.call(zoom);

      var render = new dagreD3.render();
      render(inner, this.g);

      if (!this.nodes.length) return
      
      //Events    
      if (this.selectable) {
        inner.selectAll("g.node")
        .on("click", e => {
            this.toggleSelected(e)
        })
      }
/*   .on('mouseover', debounce( e => {
          let curNode = g.node(e)
          console.log(curNode, 'curNode')
      }, 200, {leading:false, trailing:true})); */

      // Initialize zoom ratio
      var initialScale = (svg.attr("width") - 100) / this.g.graph().width;
      if (initialScale > 1)
        initialScale = 1

      // Set width and height and position
      svg.call(
          zoom.transform,
          d3.zoomIdentity
              .translate(
                  this.centered ? (svg.attr("width") - this.g.graph().width * initialScale )  / 2  : 20,
                  20
              )
              .scale(initialScale)
      );
      svg.attr("height", this.g.graph().height * initialScale  + 40)
      // Disable user zoom
      svg.on("wheel.zoom", null)
      svg.on("dblclick.zoom", null)
      // Disable drag
      svg.on("mousedown.zoom", null)
     
    },
    refresh() {
      if (this.$refs.container.clientWidth) {
        this.createLayout()
        this.drawChart()
      }     
    },    
  },
  created() {
    window.addEventListener("resize", this.resizeHandler)
    this.id = nanoid(6)
  },
  mounted() {
    if (this.nodes.length) {
      this.refresh()
    }
  },
  destroyed() {
    window.removeEventListener("resize", this.resizeHandler);
  },
  watch: {
    nodes(newVal, oldVal) {
      this.createLayout()
      this.drawChart()
    },
    selected(newVal, oldVal) {
      if (!isEqual(sortBy(newVal), sortBy(oldVal))) {
        var renamed = []
        newVal.forEach(id => {
          renamed.push(this.addIdPrefix(id))
        })
        this.clearSelected()
        renamed.forEach(nodeId => this.paintSelected(nodeId))
        this.selectedNodes = renamed
      }
    }, 
    selectedNodes() {
      var nodesWithoutPrefix = []
      this.selectedNodes.forEach(nodeId => {
        nodesWithoutPrefix.push(this.removeIdPrefix(nodeId))
      })
      this.$emit('selected', nodesWithoutPrefix)
    }
  },
};
</script>
