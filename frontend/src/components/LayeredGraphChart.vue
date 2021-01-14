<template>
  <div class="">
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
    data() {
        return {
            resizeHandler: debounce(this.drawChart, 300),
            g: undefined,
            
            nodes: [
                {
                    id: "1",
                    label: "Input data",                    
                },
                {
                    id: "2",
                    label: "Transformer 1",
                },
                {
                    id: "3",
                    label: "Transformer 2",
                },
                {
                    id: "4",
                    label: "Transformer 3 ",
                },
                {
                    id: "5",
                    label: "Detector 1",
                },
                {
                    id: "6",
                    label: "Detector 2",
                },
                {
                    id: "7",
                    label: "Detector 3",
                },
                {
                    id: "8",
                    label: "AND aggregator",
                },
                {
                    id: "9",
                    label: "OR aggregator",
                },
                {
                    id: "10",
                    label: "Output data",
                },
            ],
            edges: [
                {
                    source: "1",
                    target: "2",
                },
                {
                    source: "1",
                    target: "3",
                },
                {
                    source: "2",
                    target: "4",
                },
                {
                    source: "1",
                    target: "5",
                },
                {
                    source: "4",
                    target: "6",
                },
                {
                    source: "3",
                    target: "7",
                },
                {
                    source: "5",
                    target: "8",
                },
                {
                    source: "6",
                    target: "8",
                },
                {
                    source: "8",
                    target: "9",
                },
                {
                    source: "7",
                    target: "9",
                },
                {
                    source: "9",
                    target: "10",
                }
            ]
            
        };
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
            this.g.node(item.id).style = 'fill:' + 'green' + ';stroke: green;'
        });
        // Link relationship
        this.edges.forEach(item => {
            this.g.setEdge(item.source, item.target, {
                // Condition word on the connection
                label: item.label,
                // The color of the connection
                style: "stroke: #0fb2cc; fill: none;",
                // Arrow color
                arrowheadStyle: "fill: #0fb2cc;stroke: #0fb2cc;",
                // Arrow shape (vee means that the arrow is pointed, the default is flat)
                arrowhead: 'vee',
            });
        });
      },

      drawChart() {
        //Draw graphics
        var svg = d3.select("svg")
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
      },
    },
    created() {
      window.addEventListener("resize", this.resizeHandler)
    },
    destroyed() {
      window.removeEventListener("resize", this.resizeHandler);
    },
    mounted() {
      this.createLayout()
      this.drawChart()
   /*     //Get D3
        var g = new dagreD3.graphlib.Graph().setGraph({});

        g.graph().rankDir = 'LR';
        // add node
        this.list.nodeInfos.forEach((item, index) => {
            item.rx = item.ry = 5;//Rounded corners
            g.setNode(item.id, item);
            // node color fill refers to the background color of the node, stroke refers to the stroke color of the node
            g.node(item.id).style = 'fill:' + 'green' + ';stroke: green;'
        });
        // Link relationship
        this.list.edges.forEach(item => {
            g.setEdge(item.source, item.target, {
                // Condition word on the connection
                label: item.label,
                // The color of the connection
                style: "stroke: #0fb2cc; fill: none;",
                // Arrow color
                arrowheadStyle: "fill: #0fb2cc;stroke: #0fb2cc;",
                // Arrow shape (vee means that the arrow is pointed, the default is flat)
                arrowhead: 'vee',
            });
        }); 

        //Draw graphics
        var svg = d3.select("svg")
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
        render(inner, g);


        //Events
        inner.selectAll("g.node")
        .on("click", debounce(e => {
            this.list.nodeInfos.filter(item => {
                return item.id == e;
            });
        }, 200, {leading:false, trailing:true}))
        .on('mouseover', debounce( e => {
            let curNode = g.node(e)
            console.log(curNode, 'curNode')
        }, 200, {leading:false, trailing:true}));
        

        // Initialize zoom ratio
        var initialScale = (svg.attr("width") - 100) / g.graph().width;
        if (initialScale > 1)
          initialScale = 1

        // set width and height
        svg.call(
            zoom.transform,
            d3.zoomIdentity
                .translate(
                    (svg.attr("width") - g.graph().width * initialScale )  / 2 ,
                    20
                )
                .scale(initialScale)
        );


       // svg.attr("height", window.innerHeight)

        svg.attr("height", g.graph().height * initialScale  + 40);  */
    }
};
</script>


<style>


</style>