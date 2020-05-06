<template>
  <highcharts class="char-sec" :constructor-type="'stockChart'" :options="chartOptions" :updateArgs="updateArgs" ref="chart"></highcharts>
</template>


<script>

export default {
  props: {   
    series: {
      type: Array,
      default: []
    },
    numAxes: {
      type: Number,
      default: 1    
    },
    backgroundColor: {
      type: String,
      default: ''
    },
    isLoading: {
      type: Boolean,
      default: false
    }
  },
  data () {
    return {
      updateArgs: [true, true, {duration: 1000}],
    }
  },
  computed: {
    isEmpty() {
      return this.series.length > 0
    },
    axisOptions() {
      let axes = []
      let axisHeightPercent = Math.floor(100 / this.numAxes)
      let remainder = 100 % this.numAxes
      for (var i = 0; i < this.numAxes; i++) {
        axes.push({
          title: '',
          offset: false,
          opposite: true,
          resize: (i<this.numAxes-1) ? {
            enabled: true,
            lineColor: 'gray',
            lineWidth: 2,
          } : undefined,
          crosshair: {
            snap: !this.isEmpty,
            color: 'gray',
            dashStyle: 'shortdot',
            label: {
              backgroundColor: '#001f27',
              enabled: true,
              format: '{value:.0f}'
            }
          },
          labels: {
            align: 'left',           
          },
          // settings for multiple panes in the chart
          height: i==this.numAxes-1 ? '' + (axisHeightPercent + remainder) + '%' : '' + axisHeightPercent + '%' ,
          top: '' + (i * axisHeightPercent) + '%',    
        })
      }
      return axes
    },
    chartOptions() {
      return {
        chart: {
          zoomType: 'x',
          panning: true,
          panKey: 'shift',
          backgroundColor: this.backgroundColor,
          ignoreHiddenSeries: false,
          marginRight: 50,          
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
          text: ''
        },       
        tooltip: {
          split: true,
          shared: false,
          backgroundColor: '#001f27',
        },    
        legend: {
          enabled: false,
          align: 'left',
          itemMarginBottom: 10,
          verticalAlign: 'top',
          floating: false,
          layout: 'vertical',
          width: 150,
        },     
        xAxis: {
          crosshair: {
            color: 'gray',
            dashStyle: 'shortdot',            
          },
          type: 'datetime',
          showEmpty: false
        },   
        yAxis: this.axisOptions,
        series: this.series     
      }
    },
  },
  methods: {    
  
  },
  watch: {
    isLoading(newVal) {
      if (newVal) 
        this.$refs.chart.chart.showLoading()
      else 
        this.$refs.chart.chart.hideLoading()
    }
  }
}

</script>



<style scoped>



</style>