<template>
<div>
  <highcharts class="chart chart-section" :constructor-type="'stockChart'" :options="chartOptions" :updateArgs="updateArgs" ref="chart"></highcharts>

  
  <div class="chart-footer chart-section">
    <div class="chart-footer-section">
      <div class="chart-footer__field">
        <label class="checkbox label">
          <input type="checkbox" :checked="showBaseline" v-model="showBaseline">
          Show baseline
        </label>
      </div>
      <div class="chart-footer__field">
   <!--     <label class="label"> Score threshold</label>
        <input class="slider is-marginless" type="range" step="1" min="0" max="100" 
              v-model="scoreValue" 
              @change="changeSeriesOptions({scoreThreshold: $event.target.value})">
        <label class="tag is-info label"> {{ scoreValue }}</label>   -->

      </div>
    </div>



  </div>
</div>

</template>


<script>

export default {
     props: {   
      seriesData: {
        type: Array,
        default: []
      },
      anomalies: {
        type: Array,
        default: []
      },
      baseline: {
        type: Array,
        default: []
      },
      loading: {
        type: Boolean,
        default: false
      },
    },
    data() {
      return {
        updateArgs: [true, true, {duration: 1000}],
        scoreValue: 0,
        showBaseline: true,
      }
    },
    computed: {
      chartData() {
        return [ 
            {
              name: 'Value',
              data: this.seriesData,
              zIndex: 1,
              color: 'lightblue',
            },
            {
              name: 'Expected',
              type: 'arearange',
              data: this.chartBaseline,
              zIndex: 0,
              lineWidth: 0,
              linkedTo: ':previous',
              fillOpacity: 0.3,
              color: 'lightblue',

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
          anoms.push({id: item.id,
                     from: item.from,
                     to: item.to,
                     color: 'red',
                     events: {
                      click: function(e) {
                        vm.setActiveAnomaly(this.options.id)
                      } 
                     }
                    })
        }
        return anoms
      },
      chartBaseline() {
        return this.showBaseline ? this.$store.state.analysis.results.baseline : []
      },
      chartOptions() {
        return {
          chart: {
            zoomType: 'x',
            panning: true,
            panKey: 'shift',
            backgroundColor: "#073642",
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
        this.$store.dispatch('analysis/setActiveAnomaly', id)
      }
    },
    watch: {
      loading() {
          if (this.loading) {
            this.$refs.chart.chart.showLoading()
          } else {
            this.$refs.chart.chart.hideLoading()
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