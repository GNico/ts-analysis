<template>
  <highcharts class="chart" :constructor-type="'stockChart'" :options="chartOptions" :updateArgs="updateArgs" ref="chart"></highcharts>
</template>

<script>


export default {
  props: {
    seriesData: {
      type: Array,
      default: []
    },
    title: {
        type: String,
        default: ''
    },
    anomalies: {
        type: Array,
        default: []
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
          plotBands: this.anomalies,
          /*plotBands: [{"id": 0, "from": 1509667200000, "to": 1511568000000, "color": 'orange'}, {"id": 1, "from": 1514764800000, "to": 1514851200000 , "color": 'orange' }, {"id": 2, "from": 1519171200000, "to": 1525478400000 , "color": 'orange'}, {"id": 3, "from": 1530576000000 , "to": 1533168000000, "color": 'orange'}, {"id": 4, "from": 1539561600000 , "to": 1540339200000 , "color": 'orange'}], */
          // plotLines: this.lines
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
        series: [
          {
            data: this.seriesData

          }
        ],
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

