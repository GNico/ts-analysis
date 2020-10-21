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
    syncCrosshairEnabled: {
      type: Boolean,
      default: false
    },
    syncCrosshair: {
      type: Object,
      default: () => {}
    },
    extremes: {
      type: Object,
      default: () => { return {} }
    }, 
    loading: {
      type: Boolean,
      default: false
    },
    backgroundColor: {    //refact
      type: String,
      default: "",
    },
    lineWidth: {
      type: Number,
      default: 2
    },
    colors: {
      type: Object,
      default: () => {}
    },
  },
  data () {
    return {
      updateArgs: [true, true, false],
    }
  },
  computed: {
    interactiveBands() {
      var vm = this
      var bands = []
      for (var item of this.bands) {
        bands.push({ id: item.id,
                    from: item.from,
                    to: item.to,
                    color: this.backgroundColor,
                    events: {
                      click: function(e) {
                        vm.setActiveAnomaly(this.options.id)
                      }, 
                      mouseover: function(e) {
                        if (this.id != vm.activeAnomaly) {
                          this.svgElem.attr('fill', 'rgba(173,216,230,0.3)');
                        }
                      },
                      mouseout: function(e) {
                        if (this.id != vm.activeAnomaly) {
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
        chart: {          
          zoomType: 'x',          
          panning: true,
          panKey: 'shift',
          height: 300,
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
          backgroundColor: this.backgroundColor,
        },
        credits: false,      
        xAxis: {
          type: 'datetime',
          plotBands: this.interactiveBands,
          events: {
            setExtremes: function(event) {
              if (this.zoomEnabled && event.trigger !== 'sync') {
                vm.$emit("changedExtremes", event);
              }             
            }     
          },   
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
          //backgroundColor: '#001f27',
        },  
        plotOptions: {
          series: {
            animation: false,
            lineWidth: this.lineWidth,
            states: {
               hover: {
                  lineWidth: this.lineWidth
               },          
            },
            point: {
              events: {
                mouseOver: function(event) {
                  if (vm.syncCrosshairEnabled) {
                    vm.$emit('crosshair', {chart: vm.$refs.chart.chart, x: event.target.x, type: 'over'})
                  }
                },
                mouseOut: function(event) {
                  if (vm.syncCrosshairEnabled) {
                    vm.$emit('crosshair', {chart: vm.$refs.chart.chart, x: event.target.x, type: 'out'})
                  }
                }
              }
            }
          }
        },         
        series: {        
          data: this.seriesData,      
        }
      }
    },
  },
  methods: {
    setActiveBand(id) {
      this.$emit('changeActiveBand', id)
    },
    setChartExtremes(min, max) {
      var chart = this.$refs.chart.chart
      if (chart.xAxis[0].setExtremes) { // It is null while updating
        chart.xAxis[0].setExtremes(min, max, undefined, false, {trigger: 'sync'})
        if (chart.resetZoomButton != undefined) { // force hide or show reset button 
          if ((min == undefined || min == chart.xAxis[0].dataMin) && 
              (max == undefined) || (max == chart.xAxis[0].dataMax)) {
            chart.resetZoomButton.hide()
          } else {
            chart.resetZoomButton.show()
          }
        }
      }                      
    }, 
    selectAreaByDrag(e) {
      if (typeof e.xAxis == 'undefined')  { //reset button clicked
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
          color: 'rgba(0,0,0,0.5)',
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
    loading() {
      if (this.loading) {
        this.$refs.chart.chart.showLoading()
      } else {
        this.$refs.chart.chart.hideLoading()
      }
    },
    extremes(newVal) {
      this.setChartExtremes(newVal.min, newVal.max)
    },
    labelContent() {
      var chart = this.$refs.chart.chart
      if (chart.customTooltip) { // destroy the old one when rendering new
        chart.customTooltip.destroy()
        chart.customTooltip = undefined
      }
      var text = '<div style="color: #F0F0F0; overflow-y: scroll; max-height: ' + chart.chartHeight/4 + 'px;">'
      text += this.labelContent + '</div>'
      chart.customTooltip = chart.renderer.label(text, chart.plotSizeX /2, chart.plotTop, 'rect', undefined, undefined, true)
      .attr({ 
        'stroke-width': 1,
        zIndex: 8,
        stroke: '#F0F0F0',
        r: 3,
        fill: 'rgba(0,0,0,0.85)'
      })     
      .add()
      //.add(chart.rGroup)
      //chart.rGroup.translate(-chart.customTooltip.width / 2, -chart.customTooltip.height + 40).toFront()
    },
    syncCrosshair() {
      if (chart === this.syncCrosshair.chart) return;
     // var pointstorefresh = []
      var chart = this.$refs.chart.chart
      chart.series.forEach((series) => {
        series.points.forEach((point) => {
          if (point.x === this.syncCrosshair.x) {
            if (this.syncCrosshair.type === 'over') {
              point.setState('hover');
              point.state = '';
              //pointstorefresh.push(point)
              chart.xAxis[0].drawCrosshair(null, point);
              chart.tooltip.refresh([point]);

            } /*else {
            point.setState();
              chart.tooltip.hide();
              chart.xAxis[0].hideCrosshair();
             
            }*/
          }
        })
      })
      //if (pointstorefresh.length > 0)
      //  chart.tooltip.refresh(pointstorefresh);
    }
  },
}

</script>


<style>

.highcharts-tooltip {
  pointer-events: auto !important;
}


</style>