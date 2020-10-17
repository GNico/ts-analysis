<template>
  <highcharts class="char-sec" :constructor-type="'stockChart'" :options="chartOptions" :updateArgs="updateArgs" ref="chart"></highcharts>
</template>


<script>
import api from "../api/repository";

export default {
  props: {
    chartData: {
      type: Array,
      default: () => { return [] }
    },
    popularTags: {
      type: Array,
      default: () => { return [] }
    },
  },
  data () {
    return {
      updateArgs: [true, true, false],
      zoomEnabled: true,
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
            },      
            selection: this.selectAreaByDrag,
            click: this.unselectByClick,
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
          }
        },  
        series: {        
          data: this.chartData,      
        }
      }
    },
  },
  methods: {
    selectAreaByDrag(e) {
      if (typeof e.xAxis == 'undefined') { //reset button clicked
        return true
      }
      if (this.zoomEnabled) {
        return true
      } else {                
        this.$refs.chart.chart.xAxis[0].removePlotBand('selection')
        var min = Math.round(e.xAxis[0].min)
        var max = Math.round(e.xAxis[0].max)
        this.$refs.chart.chart.xAxis[0].addPlotBand({
          id: 'selection',
          from: min,
          to: max,
          color: '#FCFFC5',
        })
        this.$emit('selection', {min: min, max: max})
        return false
      }    
    },
    unselectByClick() {
      var chart = this.$refs.chart.chart
      if (!this.zoomEnabled) {
        if (chart.customTooltip) {
          chart.customTooltip.destroy()
          chart.customTooltip = undefined
        }
        chart.xAxis[0].removePlotBand('selection')
      }
    }
  },
  watch: {
    popularTags() {
      var chart = this.$refs.chart.chart
      if (chart.customTooltip) { // destroy the old one when rendering new
        chart.customTooltip.destroy()
        chart.customTooltip = undefined
      }
      var text = '<div class="tooltip" style="color: blue; overflow-y: scroll; border-color: yellow;">'
      for (var elem of this.popularTags) {
        text += elem.tag + ': ' + elem.count + ' <br>'
      }
      text += "</div>"
      chart.customTooltip = chart.renderer.label(text, chart.plotSizeX - 300, 200, 'rect', undefined, undefined, true)
          //chart.plotTop + point.plotY // point.y)
      .attr({ 
        'stroke-width': 1,
        zIndex: 8,
        stroke: 'black',
        //padding: 8,
        r: 3,
        fill: 'red'
      })     
      .add(chart.rGroup)

      chart.rGroup.translate(-chart.customTooltip.width / 2, -chart.customTooltip.height + 40).toFront()
    }
  },
  created() {
    window.addEventListener('keydown', (e) => {
      if (e.key == 'Control') {
        this.zoomEnabled = !this.zoomEnabled;
      }
    });
  },
}

</script>


<style>

.highcharts-tooltip {
  pointer-events: auto !important;
}

.tooltip { 
  max-height: 200px;
}

</style>