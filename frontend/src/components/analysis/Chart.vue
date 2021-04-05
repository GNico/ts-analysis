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
  :syncCrosshairEnabled="syncCrosshairEnabled"/>
</template>


<script>
import { DefaultChartSettings } from '../../config/settings'
import BaseChart from "../BaseChart";
import debounce from "lodash/debounce";


export default {
  components: { BaseChart },
  inject: ['sharedState'],
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
    chartData() {
      var cdata = []
      if (this.seriesData.length > 0) {
        cdata.push({
          name: 'Value',
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
    }
  },
  created() {
    this.triggerZoomUpdate = debounce(this.triggerZoomUpdate, 400, {'leading': true, 'trailing': false})
    this.triggerMwheelzoomUpdate = debounce(this.triggerMwheelzoomUpdate, 400, {'leading': false, 'trailing': true})
  },
}
</script>
