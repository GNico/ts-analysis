<template>
    <highcharts class="chart" :options="chartOptions" :updateArgs="updateArgs"></highcharts>
</template>

<script>


export default {
  props: {
    chartData: {
        default: [],
    },
    title: {
        type: String,
        default: ''
    },
    chartType: {
        type: String,
        default: 'line'
    },
    color: {
        type: String,
        default: '#6fcd98'
    },  
  },  
  data () {
    return {
      updateArgs: [true, true, {duration: 1000}],
    }
  },
  computed: {
    chartOptions() {
        return {
            chart: {
              type: this.chartType,
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
              data: this.chartData,
              color: this.color
            }]
        }
    } 
  }
}
</script>

