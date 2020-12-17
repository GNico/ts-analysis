<template>
 <BaseChart 
  :seriesData="chartData" 
  :bands="anomalies"
  :activeBand="activeAnomaly"
  :zoomEnabled="zoomEnabled"
  :loading="loading"
  :backgroundColor="backgroundColor"
  @changeActiveBand="setActiveAnomaly"
  @changedExtremes="updateExtremes"
  :extremes="extremes"
  />
</template>


<script>
import BaseChart from "./BaseChart";

export default {
  components: { BaseChart },
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
    backgroundColor: {
      type: String,
      default: "#073642",
    },
    seriesColor: {
      type: String, 
      default: '#e7ec98'
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
    }
  },
  data() {
    return {
      scoreValue: 0,
      labelContent: '',
      zoomEnabled: true,
      
    }
  },
  computed: {
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
          fillOpacity: 0.3,
          color: this.seriesColor,
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
      this.$emit('updateRange', { start: Math.round(event.min), end: Math.round(event.max) })
    } 
  },
  watch: {
    activeAnomaly(newId) {
      /*let axis = this.$refs.chart.chart.axes[0]
      for (var i = 0; i < axis.plotLinesAndBands.length; i++) {
        var band = axis.plotLinesAndBands[i]
        if (band.id === newId) {
          band.svgElem.attr('fill', 'rgba(173,216,230,0.3)')
        } else {
          band.svgElem.attr('fill', 'transparent')
        }
      } */
    }
  },
  created() {
   
  },
}
</script>


<style>
.chart-section {
  margin-bottom: 0.25rem;
}

.chart-section > * {
  margin: 0 0.5rem 0.5rem 0
}

.chart-footer {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  margin-right: -1rem;
}

.chart-footer-section {
  display: flex;
  align-items: baseline; 
}

.chart-footer__field {
  display: flex;
  align-items: baseline;
  margin-right: 1rem;
}

.chart-footer__field > .label {
  margin-left: 0.25rem;
  margin-right: 0.25rem;
}  

.color-box {
  visibility: hidden;
}
</style>
