<template>
  <highcharts 
    class="char-sec" 
    :constructor-type="'stockChart'" 
    :options="chartOptions" 
    :updateArgs="updateArgs" 
    :deepCopyOnUpdate="false"
    ref="chart"
    @wheel.native="wheelZoom"
  />
</template>


<script>
import { DefaultChartSettings } from '../config/settings.js'
import { nanoid } from 'nanoid'

import Highcharts from 'highcharts'

function sum(arr) {
  var sum =  arr.reduce(function (s, res) {
    return s + res;
  }, 0);  
  return sum;
}

export default {
  props: {
    seriesData: {
      type: Array,
      default: () => { return [] }
    },
    bands: {
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
    extremes: {
      type: Object,
      default: () => { return {} }
    }, 
    syncCrosshairEnabled: {
      type: Boolean,
      default: false
    },
    crosshair: {
      type: Object,
      default: () => { return {} }
    },
    activeBand: {
      type: String,
    },
    loading: {
      type: Boolean,
      default: true
    },
    settings: {
      type: Object,
      default: () => { return {} }
    },
  },
  data () {
    return {
      updateArgs: [true, true, false],
      arrows: undefined,
      cursorPosition: 0,
      eventUnbinder: null,
    }
  },
  computed: {
    normalizedSettings() {
      return {
        backgroundColor: this.settings.hasOwnProperty("backgroundColor") ? 
          this.settings.backgroundColor : DefaultChartSettings.BACKGROUND_COLOR,
        anomalyColor: this.settings.hasOwnProperty("anomalyColor") ? 
          this.settings.anomalyColor : DefaultChartSettings.ANOMALY_COLOR,
        anomalyArrowColor: this.settings.hasOwnProperty("anomalyArrowColor") ? 
          this.settings.anomalyArrowColor : DefaultChartSettings.ANOMALY_ARROW_COLOR,
        highlightedColor: this.settings.hasOwnProperty("highlightedColor") ? 
          this.settings.highlightedColor : DefaultChartSettings.HIGHLIGHT_ANOMALY_COLOR,
        highlightedBorderColor: this.settings.hasOwnProperty("highlightedBorderColor") ? 
          this.settings.highlightedBorderColor : DefaultChartSettings.HIGHLIGHT_ANOMALY_BORDER_COLOR,
        selectBandColor: this.settings.hasOwnProperty("selectBandColor") ? 
          this.settings.selectBandColor : DefaultChartSettings.SELECTION_BAND_COLOR,
        lineWidth: this.settings.hasOwnProperty("lineWidth") ? 
          this.settings.lineWidth : DefaultChartSettings.LINE_WIDTH,
        marginTop: this.settings.hasOwnProperty("marginTop") ? 
          this.settings.marginTop : DefaultChartSettings.MARGIN_TOP,
        marginBottom: this.settings.hasOwnProperty("marginBottom") ? 
          this.settings.marginBottom : DefaultChartSettings.MARGIN_BOTTOM,
        marginLeft: this.settings.hasOwnProperty("marginLeft") ? 
          this.settings.marginLeft : DefaultChartSettings.MARGIN_LEFT,
      }
    },
    isEmpty() {
      return this.seriesData.length == 0
    },
    interactiveBands() {
      var vm = this
      var bands = []
      for (var item of this.bands) {
        bands.push({ 
          id: item.id,
          from: item.from,
          to: item.to,
          color: (item.id == this.activeBand) ? this.normalizedSettings.highlightedColor : this.normalizedSettings.anomalyColor, 
          borderWidth: (item.id == this.activeBand) ? 2 : 0,
          borderColor:  (item.id == this.activeBand) ? this.normalizedSettings.highlightedBorderColor : '',
          zIndex: 0,
          events: {
            click: function(e) {              
              if (vm.activeBand == this.options.id) {
                vm.setActiveBand('')
              } else {
                vm.setActiveBand(this.options.id)
              }
            }, 
            mouseover: function(e) {
              if (this.id != vm.activeBand) {
                this.svgElem.attr('fill', vm.normalizedSettings.highlightedColor);
              }
            },
            mouseout: function(e) {
              if (this.id != vm.activeBand) {
                this.svgElem.attr('fill', this.options.color);
              }
            } 
          }
        })
      }
      return bands
    },
    chartOptions() {      
      var vm = this
      return {      
        boost: {
          enabled: false,
        },
        chart: {          
          zoomType: 'x',          
          panning: true,
          panKey: 'shift',
          animation: false, 
          ignoreHiddenSeries: false,
          showAxes: false,
          spacingLeft: this.normalizedSettings.marginLeft, 
          spacingTop: this.normalizedSettings.marginTop,  
          spacingBottom: this.normalizedSettings.marginBottom,
          backgroundColor: this.normalizedSettings.backgroundColor,
          resetZoomButton: {
            theme: {
              zIndex: 20,
              fill: 'white',
              stroke: 'silver',
              r: 0,
              states: {
                hover: {
                  fill: '#41739D',
                  style: {
                    color: 'white'
                  }
                }
              }
            }
          },
          events: {
            load: function() {
              //this.rGroup = this.renderer.g('rGroup').add() // create an SVG group to allow translate
            },      
            selection: this.selectAreaByDrag,
            click: this.unselectByClick,
          },
        },
        credits: false,  
        loading: {
          labelStyle: {
              color: 'white',
              fontSize: '1.5rem'
          },
          style: {
              backgroundColor: 'black'
          }
        },    
        xAxis: {
          allowDecimals: false,
          ordinal: false,
          gridLineWidth: 0, 
          crosshair: {
            color: 'gray',
            dashStyle: 'shortdot',            
          },
          type: 'datetime',
          showEmpty: false,
          plotBands: this.interactiveBands,
        },
        yAxis: {
          crosshair: {
            allowDecimals: false,
            snap: this.isEmpty,
            color: 'gray',
            dashStyle: 'shortdot',
            showEmpty: false,
            label: {
              backgroundColor: 'rgba(0,0,0,0.85)',
              enabled: true,
              format: '{value:.0f}'
            }
          },
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
        },  
        plotOptions: {
          arearange: {
            dataGrouping: {
              enabled: true,
              groupPixelWidth: 6,
              smoothed: true,
              approximation: function (low, high) {
                return [sum(low), sum(high)];
              },
            }
          },
          series: {
            dataGrouping: {
              enabled: true,
              groupPixelWidth: 6,
              smoothed: true,
              approximation: 'sum'
            },
            animation: false,
            lineWidth: this.normalizedSettings.lineWidth,
            point: {
              events: {
                mouseOver: function(event) {
                  vm.cursorPosition = event.target.x
                  if (vm.syncCrosshairEnabled) {
                    vm.$emit('crosshairMove', {chart: vm.$refs.chart.chart, x: event.target.x, type: 'over'})
                  }
                },              
              }
            }
          }
        },         
        series: this.seriesData,
      }
    },
  },
  methods: {
    setActiveBand(id) {
      this.$emit('changeActiveBand', id)
    },
    setChartExtremes(min, max) {
      var chart = this.$refs.chart.chart
      chart.xAxis[0].setExtremes(min, max, undefined, false, {trigger: 'sync'})
      if (chart.resetZoomButton != undefined) { // force hide or show reset button 
        if ((min == undefined || min == chart.xAxis[0].dataMin) && 
            (max == undefined) || (max == chart.xAxis[0].dataMax)) {
          chart.resetZoomButton.hide()
        } else {
          chart.resetZoomButton.show()
        }
      }
    }, 
    //return true for zoom, false to prevent zoom
    selectAreaByDrag(e) {   
      if (typeof e.xAxis == 'undefined')  { //reset button clicked
        return true
      }
      if (this.zoomEnabled) {
        return true
      } else {                
        this.$refs.chart.chart.xAxis[0].removePlotBand('selection')
        let min = e.xAxis[0].min
        let max = e.xAxis[0].max
        this.$refs.chart.chart.xAxis[0].addPlotBand({
          id: 'selection',
          from: min,
          to: max,
          color: this.normalizedSettings.selectBandColor,
        })
        this.$emit('selection', {min: min, max: max})   
        return false
      }    
    },
    unselectByClick() {
      let chart = this.$refs.chart.chart
      if (!this.zoomEnabled) {
        if (chart.customTooltip) {
          chart.customTooltip.destroy()
          chart.customTooltip = undefined
        }
        chart.xAxis[0].removePlotBand('selection')
      }
    },
    drawArrows() {
      this.clearArrows()
      if (!this.activeBand) return
      let chart = this.$refs.chart.chart
      let axis = chart.xAxis[0]
      for (let i = 0; i < axis.plotLinesAndBands.length; i++) { 
        let band = axis.plotLinesAndBands[i]
          if (band.id === this.activeBand) {
            this.arrows = chart.renderer.text('→', chart.xAxis[0].toPixels(band.options.from, true) - 20, 20)
            .attr({
            })
            .css({
                color: this.normalizedSettings.anomalyArrowColor,
                fontSize: '20px'
            })
            .add();
          }
      }
    },
    clearArrows() {
      if (this.arrows) {
        this.arrows.destroy()
      }
      this.arrows = undefined
    },
    wheelZoom(event) {
      if (!this.zoomEnabled) return
      event.preventDefault()
      var sensitivity = 0.7
      var zoomAmount = (event.deltaY > 0) ?  (1 / sensitivity) : sensitivity
      var chart = this.$refs.chart.chart
      var dataMin = chart.xAxis[0].dataMin
      var dataMax = chart.xAxis[0].dataMax
      var min = Math.round(chart.xAxis[0].min)
      var max = Math.round(chart.xAxis[0].max)
      var diff = max - min 
      var newZoomedDiff = Math.round(diff * zoomAmount)
      if (newZoomedDiff > (dataMax - dataMin)) {
        chart.xAxis[0].setExtremes(undefined, undefined, undefined, false, {trigger: 'mwheelzoom'})
        return
      }
      if (this.cursorPosition < min || this.cursorPosition > max) { 
        this.cursorPosition = min + (diff / 2)
      }
      var cursorDistanceToMin = this.cursorPosition - min 
      var cursorPercentLeft = (cursorDistanceToMin / diff)
      var newCursorDistanceToMin = newZoomedDiff * cursorPercentLeft
      var newCursorDistanceToMax = newZoomedDiff - newCursorDistanceToMin
      var newMin = Math.round(this.cursorPosition - newCursorDistanceToMin)
      var newMax = Math.round(this.cursorPosition + newCursorDistanceToMax)
      chart.xAxis[0].setExtremes(newMin, newMax, undefined, false, {trigger: 'mwheelzoom'})
    },    
  },
  watch: {
    //adding event dynamically as a workaround for multiple callbacks highcharts issue
    //https://github.com/highcharts/highcharts/issues/6943
    chartOptions: {
      immediate: true,
      handler() {
        var vm = this
        if (this.eventUnbinder && typeof this.eventUnbinder === 'function')
          this.eventUnbinder()
        this.$nextTick(() => {
          this.eventUnbinder = Highcharts.addEvent(this.$refs.chart.chart.xAxis[0], 'afterSetExtremes',
            function(event) {
              vm.drawArrows()
              if (this.zoomEnabled && event.trigger !== 'sync') {
                vm.$emit("changedExtremes", event);
              }             
            }     
          )
        })   
      }
    },
    activeBand(newId) {
      this.drawArrows() 
    },
    extremes(newVal, oldVal) {
      if (newVal.min != oldVal.min || newVal.max != oldVal.max)
        this.setChartExtremes(newVal.min, newVal.max)
    },
    loading() {
      if (this.loading) {
        this.$refs.chart.chart.showLoading()
      } else {
        this.$refs.chart.chart.hideLoading()
      }
    },
    labelContent() {
      let chart = this.$refs.chart.chart
      if (chart.customTooltip) { // destroy the old one when rendering new
        chart.customTooltip.destroy()
        chart.customTooltip = undefined
      }
      if (!this.labelContent) return;
      var text = ''
      text += '<div style="overflow-y: scroll; max-height: ' + chart.chartHeight/3 + 'px;">'
      text += this.labelContent + '</div>'
      chart.customTooltip = chart.renderer.label(text, chart.plotSizeX /2, chart.plotTop, 'rect', undefined, undefined, true)
        .attr({ 
          zIndex: 8,
        })
        .add()
      //.add(chart.rGroup)
      //chart.rGroup.translate(-chart.customTooltip.width / 2, -chart.customTooltip.height + 40).toFront()
    },
    crosshair() {
      let chart = this.$refs.chart.chart
      if (chart === this.crosshair.chart) return;
      var points = []
      chart.series.forEach((series) => {
        var point = series.points.find(p => p.x === this.crosshair.x)
        if (point && point.hasOwnProperty('color') ) {  //if color present it means boost module is not active
            if (this.crosshair.type === 'over') {
                point.setState('hover');
                point.state = '';
                chart.xAxis[0].drawCrosshair(null, point);
                points.push(point)
              }
        }
      })
      if (points.length > 0)
        chart.tooltip.refresh(points);
    }
  },
}

</script>


<style>



</style>