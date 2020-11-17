<template>
  <highcharts class="char-sec" :constructor-type="'stockChart'" :options="chartOptions" :updateArgs="updateArgs" ref="chart"></highcharts>
</template>


<script>
import api from "../api/repository";

export default {
  props: {
    seriesData: {
      type: Array,
      default: () => [] 
    },
    anomalies: {
      type: Array,
      default: () => { return [] }
    },
    baseline: {
      type: Array,
      default: () => { return [] }
    },
    labelContent: {
      type: String,
      default: ''
    },
    zoomEnabled: {
      type: Boolean,
      default: true
    },
    colors: {
      type: Object,
      default: () => {}
    },
    loading: {
      type: Boolean,
      default: false
    },
  },
  data () {
    return {
      updateArgs: [true, true, false],
    }
  },
  computed: {
   /* normalizedColors() {
      var default = {
        background: '',
        labelBackground
      }
    }, */

    chartOptions() {
      var vm = this
      return {
        chart: {
          zoomType: 'x',
          panning: true,
          panKey: 'shift',
          height: 400,
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
          data: this.seriesData,      
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
    labelContent() {
      var chart = this.$refs.chart.chart
      if (chart.customTooltip) { // destroy the old one when rendering new
        chart.customTooltip.destroy()
        chart.customTooltip = undefined
      }
      var text = '<div style="color: lightblue; overflow-y: scroll; max-height: ' + chart.chartHeight/4 + 'px;">'
      text += this.labelContent + '</div>'
      chart.customTooltip = chart.renderer.label(text, chart.plotSizeX /2, chart.plotTop, 'rect', undefined, undefined, true)
      .attr({ 
        'stroke-width': 1,
        zIndex: 8,
        stroke: 'lightblue',
        r: 3,
        fill: 'black'
      })     
      .add(chart.rGroup)
      //chart.rGroup.translate(-chart.customTooltip.width / 2, -chart.customTooltip.height + 40).toFront()
      chart.rGroup.toFront()
    }
  },
}

</script>


<style>

.highcharts-tooltip {
  pointer-events: auto !important;
}


</style>