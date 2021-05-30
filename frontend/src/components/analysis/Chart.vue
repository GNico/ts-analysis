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
  :tooltipFormatter="tooltipFormatter"/>
</template>


<script>
import { DefaultChartSettings } from '../../config/settings'
import BaseChart from "../BaseChart"
import debounce from "lodash/debounce"
import throttle from "lodash/throttle"
import { analysisTooltipFormatter } from '../../utils/helpers'


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
    showMinMax: {
      type: Boolean,
      default: false,
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
          name: 'Average',
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
        })
        if (this.showMinMax) {
          cdata.push({
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
            }
          })
        }
      } else {
        cdata.push({          
          color: 'rgba(0,0,0,0)',
          enableMouseTracking: false,
          showInLegend: false
        })
      }
      return cdata
    },
    tooltipFormatter() {
      return analysisTooltipFormatter
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
  },
  created() {
    this.triggerZoomUpdate = debounce(this.triggerZoomUpdate, 400, {'leading': true, 'trailing': false})
    this.triggerMwheelzoomUpdate = debounce(this.triggerMwheelzoomUpdate, 400, {'leading': false, 'trailing': true})
    this.syncCrosshairs = throttle(this.syncCrosshairs, 50, {'leading': true, 'trailing': true})
  },
}
</script>
