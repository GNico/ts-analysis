<template>
  <div class="chartElem">
    <highcharts class="chart" :options="chartOptions" :updateArgs="updateArgs"></highcharts>
  </div>
</template>

<script>


export default {
  props: {
    title: {
        type: String,
        default: ''
    },
    chartType: {
        type: String,
        default: 'Line'
    },
    color: {
        type: String,
        default: '6fcd98'
    },  
  },  
  data () {
    return {
      updateArgs: [true, true, {duration: 1000}],
    }
  },
  computed: {
    series_data() {
      return this.$store.state.series.data
    },
    chartOptions() {
        return {
            chart: {
              type: 'line',
              zoomType: 'xy',
              panning: true,
            },
            title: {
              text: this.title
            },
            xAxis: {
                type: 'datetime',
            },
            yAxis: {
                title: ''
            },
            rangeSelector: {
                enabled: true
            },
            scrollbar: {
                enabled: true
            },
            series: [{
              data: this.series_data,
              color: this.seriesColor
            }]
        }
    } 
  }
}
</script>

