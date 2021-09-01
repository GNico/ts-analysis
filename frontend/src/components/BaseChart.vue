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
import { nanoid } from 'nanoid'
import Highcharts from 'highcharts'

function sum(arr) {
  var sum =  arr.reduce(function (s, res) {
    return s + res;
  }, 0);  
  return sum;
}

const defaultStyle = {
  backgroundColor: 'transparent',
  anomalyColor: 'rgba(133,176,190,0.4)',
  anomalyArrowColor: 'yellow',
  highlightedColor: 'rgba(173,216,230,0.65)',
  highlightedBorderColor: 'rgba(173,216,230,1)',
  selectBandColor: 'rgba(0,0,0,0.5)',
  lineWidth: 2,
  marginTop: 0, 
  marginBottom: 0,
  marginLeft: 0
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
    tooltipFormatter: {
      type: Function,
      default: undefined
    },
    tickInterval: {
      type: Number, 
      default: null,
    },
    styleSettings: {
      type: Object,
      default: () => { return {} }
    },
    UTCOffset: {
      type: Number,
      default: 0,
    }
  },
  data () {
    return {
      updateArgs: [true, true, false],
      cursorPosition: 0,
      eventUnbinder: null,
    }
  },
  computed: {
    normalizedSettings() {
      var settings = { ...defaultStyle }
      for (const key in this.styleSettings) {
        if (settings.hasOwnProperty(key)) {
          settings[key] = this.styleSettings[key]
        }
      }
      return settings
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
          className: 'pointer-cursor',
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
        time: {
          timezoneOffset: this.UTCOffset
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
           /* load: function() {
              this.rGroup = this.renderer.g('rGroup').add() // create an SVG group to allow translate
            },      */
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
          gridLineDashStyle: 'LongDash',
          gridLineWidth: 1, 
          gridLineColor: 'rgba(255,255,255,0.2)',
          tickInterval: this.tickInterval,
          crosshair: {
            color: 'gray',
            dashStyle: 'shortdot',            
          },
          type: 'datetime',
          showEmpty: false,
          plotBands: this.interactiveBands,
        },
        yAxis: {
          // gridLineColor: 'rgba(25,50,50,0.0)',
          // gridLineDashStyle: 'Dash',
          gridLineWidth: 0,
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
          animation: true,
          split: false,
          shared: true,
          xDateFormat: '%A, %e %b %Y, %H:%M',
          useHTML: true,
          formatter: this.tooltipFormatter        
        },  
        plotOptions: {
          arearange: {
            dataGrouping: {
              enabled: true,
              groupPixelWidth: 6,
              smoothed: true,
              approximation: 'range',             
             /* approximation: function (low, high) {
                return [sum(low), sum(high)];
              }, */
            },
          /*  tooltip: {                     
              pointFormatter: function() {
                return  '<span style="color:transparent">● </span>Min: <b>'  + this.low + '</b><br/>' +
                        '<span style="color:transparent">● </span>Max: <b>'  + this.high + '</b><br/>'
              },              
            }*/
          }, 
          line: {
            tooltip: {                     
              pointFormatter: function() {
                let val = (this.y % 1) ? parseFloat(this.y).toFixed(2) : this.y
                return '<span style="color:' + this.color + '">● </span>' +  this.series.name + ': <b>'  + val + '</b><br/>'
              },              
            } 
          },
          series: {
            dataGrouping: {
              enabled: true,
              groupPixelWidth: 6,
              smoothed: true,
              dateTimeLabelFormats: {
                hour: ['%A,  %e %b %Y, %H:%M', '%A, %e %b %Y, %H:%M', '-%H:%M'],
                day: ['%A,  %e %b %Y', '%A,  %e %b %Y', '-%A, %b %e'],
                week: ['Week from %A,  %e %b %Y', '%A,  %e %b %Y', '-%A, %b %e'],
                month: ['%B %Y', '%B', '-%B %Y'],
                year: ['%Y', '%Y', '-%Y']                  
              },
                                   
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
    setChartExtremes(min, max, trigger) {
      var chart = this.$refs.chart.chart
      chart.xAxis[0].setExtremes(min, max, undefined, false, trigger)
      //toggle reset zoom button
      this.$nextTick(() => {
        var dataMin = chart.xAxis[0].dataMin
        var dataMax = chart.xAxis[0].dataMax
        var zoomMin = chart.xAxis[0].min
        var zoomMax = chart.xAxis[0].max
        if (dataMin < zoomMin || dataMax > zoomMax) {
          if (chart.resetZoomButton == undefined) chart.showResetZoom()
        } else {
          if (chart.resetZoomButton != undefined) {
            chart.resetZoomButton.destroy()
            delete chart.resetZoomButton;
          }
        }
      })     
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
        this.setChartExtremes(undefined, undefined, {trigger: 'mwheelzoom'})
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
      this.setChartExtremes(newMin, newMax, {trigger: 'mwheelzoom'})
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
              if (this.zoomEnabled && event.trigger !== 'sync') {
                vm.$emit("changedExtremes", event);
              }             
            }     
          )
        })   
      }
    },
    activeBand(newId) {
    },
    extremes: {
      immediate: true,
      handler(newVal, oldVal) {
        if (!oldVal || (newVal.min != oldVal.min || newVal.max != oldVal.max))
          this.$nextTick(function() { 
            var chart = this.$refs.chart.chart
            var dataMin = chart.xAxis[0].dataMin
            var dataMax = chart.xAxis[0].dataMax
            var realMin = (newVal.min < dataMin) ? dataMin : newVal.min 
            var realMax = (newVal.max > dataMax) ? dataMax : newVal.max
            this.setChartExtremes(realMin, realMax, {trigger: 'sync'})
          })
        } 
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
