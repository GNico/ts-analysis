<template>
    <highcharts class="chart" :options="chartOptions" :updateArgs="updateArgs" ref="chart" @anomclicked="showmsg"></highcharts>
</template>

<script>


export default {
  props: {
    seriesData: {
        default: function () {
          return []
        }
    },
    title: {
        type: String,
        default: ''
    },
    anomalies: {
        type: Array,
        default: function () {
          return []
        }
    },
    isLoading: false,
  },  
  data () {
    return {
      updateArgs: [true, true, {duration: 1000}],
      scoreThreshold: '0',
      bands: [],
      lines: [],
    }
  },
  computed: {
    chartOptions() {
      return {
        chart: {
          zoomType: 'xy',
          panning: true,
          panKey: 'shift',
          backgroundColor: "#073642"
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
          plotBands: this.anomalies,
          // plotLines: this.lines
        },
        yAxis: {
          title: '',
        },
        rangeSelector: {
          enabled: true
        },
        scrollbar: {
          enabled: true
        },
        legend: {
          enabled: true,
        },
        series: this.seriesData
      }
    },
  },
  methods: {
    showmsg(event) {
      console.log(event)
    }
  },
  watch: {
    isLoading() {
        if (this.isLoading) {
          this.$refs.chart.chart.showLoading()
        } else {
          this.$refs.chart.chart.hideLoading()
        }
    }
    
  }
}
</script>

