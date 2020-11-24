<template>
 <BaseChart 
  :seriesData="chartData" 
  :bands="anomalies"
  :activeBand="activeAnomaly"
  @changeActiveBand="setActiveAnomaly"
  :zoomEnabled="zoomEnabled"
  :loading="loading"
  :backgroundColor="backgroundColor"/>
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
    anomalyColor: {
      type: String, 
      default: 'yellow'
    },
    activeAnomaly: {
      type: String,
    },
  },
  data() {
    return {
      scoreValue: 0,
      labelContent: '',
      zoomEnabled: true,
    }
  },
  computed: {
    colorZones() {
      var zones = []
      this.anomalies.forEach(anom => {
        var zone1 = { value: anom.from, color: this.seriesColor }
        var zone2 = { value: anom.to, color: this.anomalyColor }
        zones.push(zone1)
        zones.push(zone2)
      })
      zones.push({color: this.color})
      return zones
    },
    chartData() {
      let cdata = []
      if (this.seriesData.length > 0) {
        cdata.push({
          name: 'Value',
          data: this.seriesData,
          zoneAxis: 'x',
          zones: undefined, 
          zIndex: 2,
          color: this.seriesColor,
          states: {
            hover: {
              lineWidthPlus: 0
            }
          },
        })
      }
      if (this.baseline.length > 0) {
        cdata.push({
          name: 'Expected',
          type: 'arearange',
          data: this.baseline,
          zIndex: 1,
          lineWidth: 0,
          linkedTo: ':previous',
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
    chartOptions() {
      var vm = this
      return {
        chart: {
          zoomType: 'x',
          panning: true,
          panKey: 'shift',
          backgroundColor: this.backgroundColor,
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
        title: {
          text: this.title
        },
        xAxis: {
          type: 'datetime',
          plotBands: this.chartAnomalies,
          events: {
            setExtremes: function(event) {
              if (event.trigger !== 'sync') {                
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
          backgroundColor: '#001f27',
        },    
        series: this.chartData,
      }
    },
  },
  methods: {
    setActiveAnomaly(id) {
      this.$emit('changeActive', id)
    },    
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
    window.addEventListener('keydown', (e) => {
      if (e.key == 'Control') {
        this.zoomEnabled = !this.zoomEnabled;
      }
    });
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
