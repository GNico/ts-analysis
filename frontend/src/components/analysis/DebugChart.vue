<template>
  <highcharts 
    :options="chartOptions" 
    :deepCopyOnUpdate="false"/>
</template>


<script>
export default {
  props: {
    title: {
      type: String,
      default: ''
    },
    data: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {

    }
  },
  computed: {
    chartUTCOffset() {
      return this.$store.state.UTCOffset * -60 
    },
    chartOptions() {
      return {
        time: {
          timezoneOffset: this.chartUTCOffset
        },
        chart: {
          backgroundColor: 'transparent'
        },
        credits: false,  
        legend: {
          enabled: false,
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
        title: '',
        yAxis: {
          title: false,
          endOnTick: false,
          //max: 1,
          //min: -1,
        },
        series: [{
          name: this.title,
          data: this.data,
          type: (this.title.includes('line') ? 'line' : 'column'),
        }]
      }
    }
  }

}


</script>