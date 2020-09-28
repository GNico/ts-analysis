<template>
<div>
  <highcharts class="chart chart-section" :constructor-type="'stockChart'" :options="chartOptions" :updateArgs="updateArgs" ref="chart"></highcharts>

  
 <!--     <div class="chart-footer-section">
      <div class="chart-footer__field">
        <label class="checkbox label">
          <input type="checkbox" :checked="showBaseline" v-model="showBaseline">
          Show baseline
        </label>
      </div>
      <div class="chart-footer__field">
      <label class="label"> Score threshold</label>
        <input class="slider is-marginless" type="range" step="1" min="0" max="100" 
              v-model="scoreValue" 
              @change="changeSeriesOptions({scoreThreshold: $event.target.value})">
        <label class="tag is-info label"> {{ scoreValue }}</label>  

      </div>
    </div>
 -->


</div>

</template>


<script>

function getPlotBandOrLineById(id, axis) {
  // loop through all plotBands/plotLines and check their id
  for (var i = 0; i < axis.plotLinesAndBands.length; i++) {
    if (axis.plotLinesAndBands[i].id === id) {
      return axis.plotLinesAndBands[i];
    }
  }
}

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
      }
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
      chartAnomalies() {
        var vm = this
        var anoms = []
        for (var item of this.anomalies) {
          anoms.push({ id: item.id,
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
        return anoms
      },
      chartOptions() {
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
