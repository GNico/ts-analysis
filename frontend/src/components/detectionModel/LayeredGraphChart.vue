<template>
<div :id="id">
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
    id: {   //required for multiple instances
      type: String,
      required: true,
    },
    nodes: {
      type: Array,
      default: () => []
    },
    edges: {
      type: Array,
      default: () => []
    },
  },
  data() {
    return {
      resizeHandler: debounce(this.drawChart, 300),
      g: undefined,        
    }
  },
  methods: {
    createLayout() {
      this.g = new dagreD3.graphlib.Graph().setGraph({})
      this.g.graph().rankDir = 'LR';

      // Add node
      this.nodes.forEach((item, index) => {
        item.rx = item.ry = 5;
        this.g.setNode(item.id, item);
        this.g.node(item.id).style = 'fill:' + '#005aff' + ';stroke: white;'
        this.g.node(item.id).labelStyle = 'fill:  white;'
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
    drawChart() {
      //Draw graphics
      var svg = d3.select("#" + this.id).select("svg")
      var inner = svg.select("g");
      var thediv = document.getElementById(this.id)
      var maxWidth = thediv.clientWidth
      svg.attr("width", maxWidth)
      // Set up zoom support
      var zoom = d3.zoom().on("zoom", function () {
          inner.attr("transform", d3.event.transform);
      });
      svg.call(zoom);
      
      var render = new dagreD3.render();
      render(inner, this.g);
      if (this.nodes.length == 0) return
/*      //Events
      inner.selectAll("g.node")
      .on("click", debounce(e => {
          this.list.nodeInfos.filter(item => {
              return item.id == e;
          });
      }, 200, {leading:false, trailing:true}))
      .on('mouseover', debounce( e => {
          let curNode = g.node(e)
          console.log(curNode, 'curNode')
      }, 200, {leading:false, trailing:true})); */
      // Initialize zoom ratio
      var initialScale = (svg.attr("width") - 100) / this.g.graph().width;
      if (initialScale > 1)
        initialScale = 1
      // Set width and height
      svg.call(
          zoom.transform,
          d3.zoomIdentity
              .translate(
                  (svg.attr("width") - this.g.graph().width * initialScale )  / 2 ,
                  20
              )
              .scale(initialScale)
      );
      svg.attr("height", this.g.graph().height * initialScale  + 40); 
      // Disable user zoom
      svg.on("wheel.zoom", null);
      svg.on("dblclick.zoom", null);
    },
    refresh() {
      this.createLayout()
      this.drawChart()
    }
  },
  created() {
    window.addEventListener("resize", this.resizeHandler)
  },
  destroyed() {
    window.removeEventListener("resize", this.resizeHandler);
  },
  watch: {
    nodes() {
      this.createLayout()
      this.drawChart()
    }
  },
};
</script>


<style>


</style>