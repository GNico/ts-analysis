<template>
<BaseChart 
  :style="{height: height}"
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
  :tooltipFormatter="tooltipFormatter"
  :tickInterval="tickInterval"
  :UTCOffset="chartUTCOffset"/>
</template>


<script>
import { DefaultChartSettings } from '@/config/settings'
import BaseChart from "@/components/BaseChart"
import debounce from "lodash/debounce"
import throttle from "lodash/throttle"
import { analysisTooltipFormatter, multiseriesTooltipFormatter } from '@/utils/tooltipFormatter'


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
      type: Object,
      default: () => { return {} }
    },
    anomalies: {
      type: Array,
      default: () => []
    },
    showMinMax: {
      type: Boolean,
      default: false,
    },
    axisInterval: {
      type: String,
      default: '',
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
    forcedMaxRange: {
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
    },
    height: {
      type: [String, Number],
      default: 'inherit'
    },    
  },
  data() {
    return {
      tooltipFormatter: analysisTooltipFormatter
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
    tickInterval() {
      var tickNumber = null
      switch (this.axisInterval) {
        case "month":
          tickNumber = 28*24*3600*1000
          break
        case "week":
          tickNumber = 7*24*3600*1000
          break
        case "day": 
          tickNumber = 24*3600*1000
          break
        case "hour":
          tickNumber = 3600*1000
        default:
          tickNumber = null
          break
      }
      return tickNumber
    },
    chartData() {
      var cdata = []
      var seriesIds = Object.keys(this.seriesData)
      if (seriesIds.length == 0) { //no series
        cdata.push({          
          color: 'rgba(0,0,0,0)',
          enableMouseTracking: false,
          showInLegend: false
        })
      } else if (seriesIds.length == 1) { //1 series = show variance
        this.tooltipFormatter = analysisTooltipFormatter
        cdata.push({
          name: 'Average',
          type: 'line',
          data: this.seriesData[seriesIds[0]],
          zIndex: 3,
          fillOpacity: 1,
          enableMouseTracking: true,
          color: this.seriesColor,
          states: {
            hover: {
              lineWidthPlus: 0
            }
          },
        })
        if (this.showMinMax) {
          cdata.push({
            name: 'Range',
            type: 'arearange',
            data: this.toArearangeData(this.seriesData[seriesIds[0]]),
            zIndex: 2,
            color: this.seriesColor,
            fillOpacity: 0.3,
            enableMouseTracking: true,
            lineWidth: 0,
            states: {
              hover: {
                lineWidthPlus: 0
              }
            }
          })
        } 
      } else {  //more than 1 series, dont show variance
        this.tooltipFormatter = multiseriesTooltipFormatter
        seriesIds.forEach(seriesId => {
          cdata.push({
            name: seriesId,
            type: 'line',
            data: this.seriesData[seriesId],
            zIndex: 3,
            fillOpacity: 1,
            enableMouseTracking: true,
            states: {
              hover: {
                lineWidthPlus: 0
              }
            },
          })
        })
      }

      if (this.forcedMaxRange.start) { //invisible series to force out of bound extremes
        cdata.push({
          name: "ForceRangeStart",
          data: [{
            x: this.forcedMaxRange.start,
            y: 0
          }],
          color: 'rgba(0,0,0,0)',
          enableMouseTracking: false,
          showInLegend: false
        })
      }
      if (this.forcedMaxRange.end) { //invisible series to force out of bound extremes
        cdata.push({
          name: "ForceRangeStart",
          data: [{
            x: this.forcedMaxRange.end,
            y: 0
          }],
          color: 'rgba(0,0,0,0)',
          enableMouseTracking: false,
          showInLegend: false
        })
      }
      return cdata
    },
    chartUTCOffset() {
      return this.$store.state.UTCOffset 
    }
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
    toArearangeData(seriesData) {
      let rangedata = []
      seriesData.forEach(point => {
        rangedata.push([ point[0], point[1], point[1] ])
      })
      return rangedata
    }
  },
  created() {
    this.triggerZoomUpdate = debounce(this.triggerZoomUpdate, 400, {'leading': true, 'trailing': false})
    this.triggerMwheelzoomUpdate = debounce(this.triggerMwheelzoomUpdate, 400, {'leading': false, 'trailing': true})
    this.syncCrosshairs = throttle(this.syncCrosshairs, 50, {'leading': true, 'trailing': true})
  },
}
</script>
