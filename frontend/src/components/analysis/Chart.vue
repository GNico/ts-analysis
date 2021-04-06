<template>
<BaseChart 
  :seriesData="chartData" 
  :bands="anomalies"
  :activeBand="activeAnomaly"
  :loading="loading"
  @changeActiveBand="setActiveAnomaly"
  @changedExtremes="updateExtremes"
  :extremes="extremes" 
  @crosshairMove="syncCrosshairs"
  :crosshair="crosshair"
  :syncCrosshairEnabled="syncCrosshairEnabled"
  :tooltipFormatter="formatter"/>
</template>


<script>
import { DefaultChartSettings } from '../../config/settings'
import BaseChart from "../BaseChart";
import debounce from "lodash/debounce";
import throttle from "lodash/throttle";
import { formatDateVerbose } from '../../utils/helpers'


var formatter = function() { 
  function hourlyHeader(original, range) {
    var d = new Date(original+range)
    const hour = d.getHours().toString().padStart(2, '0')
    const minutes = d.getMinutes().toString().padStart(2, '0')
    return '<small>' + formatDateVerbose(original) + ` to ${hour}:${minutes}</small><br>`
  }
  var currentDataGrouping = this.points[0].series.currentDataGrouping
  var header = ''
  if (currentDataGrouping) {
    if (currentDataGrouping.unitName == 'day') {
      header = '<small>' + formatDateVerbose(this.x, true, false) + 
        ' to ' + formatDateVerbose(this.x + currentDataGrouping.totalRange , false, false) +'</small><br>'
    } 
    if (currentDataGrouping.unitName == 'hour') {
      header = hourlyHeader(this.x, currentDataGrouping.totalRange)
    }
  } else {
    header = hourlyHeader(this.x, this.points[0].series.closestPointRange)
  }
  let val = (this.points[0].y % 1) ? parseFloat(this.points[0].y).toFixed(2) : this.points[0].y
  var min = 'Min: <b>' + this.points[1].point.low + '</b><br>'
  var max = 'Max: <b>' + this.points[1].point.high + '</b>'  
  var text =  header 
  if (currentDataGrouping) {
    text = `${text} Avg: <b>${val}</b><br>${min}${max}`
  } else {
    text = `${text} Value: <b>${val}</b><br>`
  }
  return text
} 

export default {
  components: { BaseChart },
  inject: {
    sharedState: {
      name: 'sharedState',
      default: {}
    }
  },
  props: {   
    seriesData: {
      type: Array,
      default: () => { return [] }
    },
    anomalies: {
      type: Array,
      default: () => { return [] }
    },
    baseline: {
      type: Array,
      default: () => { return [] }
    },
    loading: {
      type: Boolean,
      default: false
    },
    seriesColor: {
      type: String, 
      default: DefaultChartSettings.SERIES_COLOR
    },
    activeAnomaly: {
      type: String,
    },
    range: {
      type: Object,
      default: () => {
        return {
          start: null,
          end: null
        }
      }
    },
    syncCrosshairEnabled: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      formatter: formatter
    }
  },
  computed: {
    crosshair() {
      return this.sharedState ? this.sharedState.crosshair : {}
    },
    extremes() {
      return {
        min: this.range.start,
        max: this.range.end
      }
    }, 
    arearangedata() {
      let newdata = []
      this.seriesData.forEach(point => {
        newdata.push([ point[0], point[1], point[1] ])
      })
      return newdata
    },

    chartData() {
      var cdata = []
      if (this.seriesData.length > 0) {
        cdata.push({
          name: 'Avg',
          type: 'line',
          data: this.seriesData,
          zIndex: 2,
          fillOpacity: 1,
          enableMouseTracking: true,
          color: this.seriesColor,
          states: {
            hover: {
              lineWidthPlus: 0
            }
          },
        },
        {
          name: 'Range',
          type: 'arearange',
          data: this.arearangedata,
          zIndex: 1,
          color: this.seriesColor,
          fillOpacity: 0.3,
          enableMouseTracking: true,
          lineWidth: 0,
          states: {
            hover: {
              lineWidthPlus: 0
            }
          },

        })
      } else {
        cdata.push({          
          color: 'rgba(0,0,0,0)',
          enableMouseTracking: false,
          showInLegend: false
        })
      }
      if (this.baseline.length > 0) {
        cdata.push({
          name: 'Expected',
          type: 'arearange',
          data: this.baseline,
          zIndex: 1,
          lineWidth: 0,
          fillOpacity: DefaultChartSettings.BASELINE_OPACITY,
          color: DefaultChartSettings.BASELINE_COLOR,
          states: {
            hover: {
              lineWidthPlus: 0
            }
          },
          marker: {
              enabled: false
          }
        })
      }
      return cdata
    },
  },
  methods: {
    setActiveAnomaly(id) {
      this.$emit('changeActive', id)
    },   
    updateExtremes(event) {
      if (event.trigger == 'zoom') {
        this.triggerZoomUpdate(event)
      } else {
        this.triggerMwheelzoomUpdate(event)
      }
    },
    triggerZoomUpdate(event) {
      this.$emit('updateRange', { start: Math.round(event.min), end: Math.round(event.max) })
    },
    triggerMwheelzoomUpdate(event) {
      this.$emit('updateRange', { start: Math.round(event.min), end: Math.round(event.max) })
    },
    syncCrosshairs(event) {
      if (this.syncCrosshairEnabled && this.sharedState) {
        this.sharedState.crosshair = event
      }
    },
  },
  created() {
    this.triggerZoomUpdate = debounce(this.triggerZoomUpdate, 400, {'leading': true, 'trailing': false})
    this.triggerMwheelzoomUpdate = debounce(this.triggerMwheelzoomUpdate, 400, {'leading': false, 'trailing': true})
    this.syncCrosshairs = throttle(this.syncCrosshairs, 50, {'leading': true, 'trailing': true})
  },
}
</script>
