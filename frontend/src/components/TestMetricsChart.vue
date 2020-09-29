<template>
  <highcharts class="chart chart-section" :constructor-type="'stockChart'" :options="chartOptions" :updateArgs="updateArgs" ref="chart"></highcharts>
</template>


<script>

export default {
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
        default: 'lightblue'
      },
      anomalyColor: {
        type: String, 
        default: 'orange'
      },
      activeAnomaly: {
        type: String,
      },
      extremes: {
        type: Object,
        default: () => { return {} }
      },
      metrics: {
        type: Array,
        default: () => { return [] }
      },   
    },
    data() {
      return {
        updateArgs: [true, true, {duration: 1000}],
        scoreValue: 0,
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
      chartBands() {
        var bands = []
        this.metrics.forEach(metric => {
            let band = {
                from: metric.from,
                to: metric.to,
                color: 'grey'
            }
            switch(metric.type) {
                case "tp": 
                    band.color = 'green'
                    break;
                case "tn":
                    band.color = 'red'
                    break;
                case "fp":
                    band.color = 'yellow'
                    break;
                case "fn":
                    band.color = 'blue'
                    break;      
                default:
                    break;  
            }
            bands.push(band)
        })
        return bands
      },
      chartData() {
        return [ 
          {
            name: 'Value',
            data: this.seriesData,
            zoneAxis: 'x',
            zones: this.colorZones, 
            zIndex: 1,
            color: this.seriesColor,
            states: {
              hover: {
                lineWidthPlus: 0
              }
            },
          },
          {
            name: 'Expected',
            type: 'arearange',
            data: this.baseline,
            zIndex: 0,
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
          }
        ]
        
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
            plotBands: this.chartBands,
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
      setChartExtremes(min, max) {
        if (this.$refs.chart.chart.xAxis[0].setExtremes) { // It is null while updating
          this.$refs.chart.chart.xAxis[0].setExtremes(min, max, undefined, false, {trigger: 'sync'} );
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
      activeAnomaly(newId) {
        let axis = this.$refs.chart.chart.axes[0]
        for (var i = 0; i < axis.plotLinesAndBands.length; i++) {
          var band = axis.plotLinesAndBands[i]
          if (band.id === newId) {
            band.svgElem.attr('fill', 'rgba(173,216,230,0.3)')
          } else {
            band.svgElem.attr('fill', this.backgroundColor)
          }
        }
      }
    }
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
