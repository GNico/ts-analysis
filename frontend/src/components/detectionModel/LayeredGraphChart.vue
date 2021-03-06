<template>
<div ref="container">
  <svg> 
    <g/>
    <rect/>
  </svg>
</div>
</template>

<script>
import dagreD3 from "dagre-d3";
import * as d3 from "d3";
import debounce from "lodash/debounce";

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
    centered: {
      type: Boolean,
      default: true,
    }
  },
  data() {
    return {
      resizeHandler: debounce(this.refresh, 300),
      g: undefined,   
      selectedNodes: [],    
    }
  },
  methods: {
    createLayout() {
      this.g = new dagreD3.graphlib.Graph().setGraph({})
      this.g.graph().rankDir = 'LR';
      // Add nodes
      this.nodes.forEach((item, index) => {
        item.rx = item.ry = 5;
        this.g.setNode(item.id, item);
        if (this.selectedNodes.includes(item.id)) {
          this.g.node(item.id).style = 'fill: green; stroke: yellow;'
          this.g.node(item.id).labelStyle = 'fill:  yellow;'
        } else {
          this.g.node(item.id).style = 'fill:#005aff; stroke: white;'
          this.g.node(item.id).labelStyle = 'fill:  white;'
        }        
      });
      // Link relationship
      this.edges.forEach(item => {
        this.g.setEdge(item.source, item.target, {
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
        this.selectedNodes.push(nodeId)
        d3.select("#" + nodeId + ' rect').attr('style', 'fill: green; stroke: yellow')
        d3.select("#" + nodeId + ' text').attr('style', 'fill: yellow;')
      } else {
        this.selectedNodes.splice(index, 1)
        d3.select("#" + nodeId + ' rect').attr('style', 'fill: #005aff; stroke: white')
        d3.select("#" + nodeId + ' text').attr('style', 'fill:  white;')
      }
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
      this.createLayout()
      this.drawChart()
    }
  },
  created() {
    window.addEventListener("resize", this.resizeHandler)
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
    nodes() {
      this.createLayout()
      this.drawChart()
    },
    selectedNodes() {
      this.$emit('selected', this.selectedNodes)
    }
  },
};
</script>


<style>


</style>