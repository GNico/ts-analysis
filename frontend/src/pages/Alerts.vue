<template>
  <highcharts class="char-sec" :constructor-type="'stockChart'" :options="chartOptions" :updateArgs="updateArgs" ref="chart"></highcharts>
</template>


<script>
import api from "../api/repository";

export default {
  data () {
    return {
      updateArgs: [true, true, false],
      chartData: [],
      popularTags: [],

      selectedPoint: {},
    }
  },
  computed: {
    chartOptions() {
      var vm = this
      return {
        chart: {
          zoomType: 'x',
          panning: true,
          panKey: 'shift',
          events: {
            load: function() {
              this.rGroup = this.renderer.g('rGroup').add() // create an SVG group to allow translate
            }
          }
          //backgroundColor: this.backgroundColor,
        },
        credits: false,      
        xAxis: {
          type: 'datetime',          
        },
        yAxis: {
          title: '',
        },
        rangeSelector: {
          enabled: false
        },
        scrollbar: {
          enabled: false
        },
        navigator: {
          enabled: false
        },
        legend: {
          enabled: false,
        },
        tooltip: {
          split: false,
          shared: true,
          valueDecimals: 0,
          backgroundColor: '#001f27',
        },  
        plotOptions: {
          series: {      
            allowPointSelect: true,
            events: {
              click: function (event) {
                var point = event.point
                var chart = point.series.chart

                if (chart.customTooltip) { // destroy the old one when rendering new
                  chart.customTooltip.destroy()
                  chart.customTooltip = undefined
                }


                var tags = vm.popularTags.find(element => element.timestamp == point.x)

                var text = ''
                for (var tag of tags.tags) {
                  text += tag.key + ': ' + tag.doc_count + ' <br>'
                }

                //var text = point.series.name + ': <strong>' + elem + '</strong> <br>' + "something  <br>something  <br>something  <br>"

                chart.customTooltip = chart.renderer.label( // render tooltip
                    text ,
                    chart.plotSizeX - 150, 40 // point.x
                    //chart.plotTop + point.plotY // point.y
                  )
                  .attr({ // style tooltip
                    'stroke-width': 1,
                    zIndex: 8,
                    stroke: point.series.color,
                    padding: 8,
                    r: 3,
                    fill: 'rgb(247, 247, 247)'
                  })
                  .add(chart.rGroup)

                chart.rGroup.translate(-chart.customTooltip.width / 2, -chart.customTooltip.height + 40).toFront()

              }  
            } 
          }
        },  


        series: {        
          data: this.chartData,      
        }
      }
    },
  },
  methods: {
    pointClicked(point) {
      console.log(point)
      var elem = this.popularTags.find(element => element.timestamp == point)
      selectedPoint = { }
    },
  },
  mounted: function () {
    api.getSeriesData({ 
        name: "treetest",
      })
      .then(response => {       
        this.chartData = response.data.series
        this.popularTags = response.data.popular_tags
      })
      .catch(error => { 
        console.log('error')
        console.log(error)
      })
  }
}

</script>