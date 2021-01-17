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

      // add node
      this.nodes.forEach((item, index) => {
        item.rx = item.ry = 5;//Rounded corners
        this.g.setNode(item.id, item);
        // node color fill refers to the background color of the node, stroke refers to the stroke color of the node
        this.g.node(item.id).style = 'fill:' + '#005aff' + ';stroke: white;'
        // node label style
        this.g.node(item.id).labelStyle = 'fill:  white;'
      });
      // Link relationship
      this.edges.forEach(item => {
        this.g.setEdge(item.source, item.target, {
          // Condition word on the connection
          label: item.label,
          // The color of the connection 0fb2cc
          style: "stroke: lightblue; fill: none; stroke-width: 1px",
          // Arrow color
          arrowheadStyle: "fill: lightblue; stroke: lightblue;",
          // Arrow shape (vee means that the arrow is pointed, the default is flat)
          arrowhead: 'vee',
        });
      });
    },

    drawChart() {
      //Draw graphics
      var svg = d3.select("#" + this.id).select("svg")
      var inner = svg.select("g");

      var maxWidth = window.innerWidth
      svg.attr("width", maxWidth)

      // Set up zoom support
      var zoom = d3.zoom().on("zoom", function () {
          inner.attr("transform", d3.event.transform);
      });
      svg.call(zoom);

      // Create the renderer
      var render = new dagreD3.render();
      // Run the renderer. This is what draws the final graph.
      render(inner, this.g);


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

      // set width and height
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
  mounted() {

  }
};
</script>


<style>


</style>