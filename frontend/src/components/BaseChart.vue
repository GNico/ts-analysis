<template>
  <highcharts class="char-sec" :constructor-type="'stockChart'" :options="chartOptions" :updateArgs="updateArgs" ref="chart"></highcharts>
</template>


<script>
import { nanoid } from 'nanoid'

function sum(arr) {
  var sum =  arr.reduce(function (s, res) {
    return s + res;
  }, 0);  
  return sum;
}


var internalFunctionId = '' //  workaround for multiple callbacks highcharts issue 
                            //  https://github.com/highcharts/highcharts/issues/6943

export default {
  props: {
    seriesData: {
      type: Array,
      default: () => [] 
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
      default: () => {}
    },
    activeBand: {
      type: String,
    },
    loading: {
      type: Boolean,
      default: true
    },
    backgroundColor: {    //refact
      type: String,
      default: '',
    },
    lineWidth: {
      type: Number,
      default: 2
    },
    margin: {
      type: Object,
      default: () => {return {
        top: 0,
        bottom: 0,
        left: 0,
      }}
    },
  },
  data () {
    return {
      updateArgs: [true, true, false],
      arrows: undefined,
    }
  },
  computed: {
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
          color: (item.id == this.activeBand) ? 'rgba(173,216,230,0.3)' : 'rgba(255,0,0,0.8)',  //red
          borderWidth: (item.id == this.activeBand) ? 2 : 0,
          borderColor:  (item.id == this.activeBand) ? 'rgba(173,216,230,1)' : '',
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
                this.svgElem.attr('fill', 'rgba(173,216,230,0.3)');
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
      var functionId = nanoid()
      internalFunctionId = functionId

      var vm = this
      return {      
        boost: {
          enabled: false,
        },
        mapNavigation: {
          enableMouseWheelZoom: true,
        },
        chart: {          
          zoomType: 'x',          
          panning: true,
          panKey: 'shift',
          animation: false, 
          ignoreHiddenSeries: false,
          showAxes: false,
          spacingLeft: this.margin.left ? this.margin.left : 0,   
          spacingTop: this.margin.top ? this.margin.top : 0, 
          spacingBottom: this.margin.bottom ? this.margin.bottom : 0, 
          backgroundColor: this.backgroundColor,
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
          ordinal: false,
          gridLineWidth: 0, 
          crosshair: {
            color: 'gray',
            dashStyle: 'shortdot',            
          },
          type: 'datetime',
          showEmpty: false,
          plotBands: this.interactiveBands,
          events: {
            afterSetExtremes: function(event) {
              if (functionId != internalFunctionId) return
              vm.drawArrows()
              if (this.zoomEnabled && event.trigger !== 'sync') {
                vm.$emit("changedExtremes", event);
              }             
            }     
          },   
        },
        yAxis: {
          crosshair: {
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
          events: {
            afterSetExtremes: function(event) {
              if (event.min || event.max)
                vm.$refs.chart.chart.yAxis[0].setExtremes(undefined, undefined, undefined, false, {trigger: 'resetYaxis'})
            }
          }
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
              approximation: function (low, high) {
                return [sum(low), sum(high)];
              },
            }
          },
          series: {
            dataGrouping: {
              enabled: true,
              approximation: 'sum'
            },
            animation: false,
            lineWidth: this.lineWidth,
            point: {
              events: {
                mouseOver: function(event) {
                  if (vm.syncCrosshairEnabled) {
                   // vm.$emit('crosshairMove', {chart: vm.$refs.chart.chart, x: event.target.x, type: 'over'})
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
          color: 'rgba(0,0,0,0.5)',
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
                color: 'yellow',
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
  /*  highlightActive() {
      this.clearArrows()
      let chart = this.$refs.chart.chart
      let axis = chart.axes[0]
      for (let i = 0; i < axis.plotLinesAndBands.length; i++) {        
        let band = axis.plotLinesAndBands[i]
        if (band.id != 'selection') {
          if (band.id === this.activeBand) {
            band.svgElem.attr('fill', 'rgba(173,216,230,0.3)').shadow({color: 'rgba(173,216,230,0.3)', opacity: 1})
            this.arrows = chart.renderer.text('→', chart.xAxis[0].toPixels(band.options.from, true) - 20, 20)
              .attr({
              })
              .css({
                  color: 'yellow',
                  fontSize: '20px'
              })
              .add();
          } else if (band.id !== undefined) {   
            band.svgElem.attr('fill', 'rgba(255,0,0,0.8)').shadow(false)        
          }
        }
      } 
    }, */
  },
  watch: {
    activeBand(newId) {
      this.drawArrows() 
      //this.highlightActive()
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