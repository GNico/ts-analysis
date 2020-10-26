<template>

<div class="fill-height-or-more">
  <BaseChart v-for="seriesData in chartSeriesData" :seriesData="seriesData" :key="seriesData.id" :loading="isLoading"/>
</div>
<!--  <highcharts class="char-sec" :constructor-type="'stockChart'" :options="chartOptions" :updateArgs="updateArgs" ref="chart"></highcharts> -->
</template>


<script>
import BaseChart from "./BaseChart";

export default {
  components: { BaseChart },
  props: {   
    series: {
      type: Array,
      default: () => []
    },
    panels: {
      type: Array,
      default: () => []
    },
    numAxes: {
      type: Number,
      default: 1    
    },
    isLoading: {
      type: Boolean,
      default: false
    },
    backgroundColor: {
      type: String,
      default: ''
    },
    lineWidth: {
      type: Number,
      default: 2
    },
    marginLeft: {
      type: Number,
      default: 100
    },
    marginTop: {
      type: Number,
      default: 0
    },
    marginBottom: {
      type: Number,
      default: 0
    },
  },
  data () {
    return {
      updateArgs: [true, true, false],
    }
  },
  computed: {
    isEmpty() {
      return this.series.length > 0
    },
    chartSeriesData() {
      let allSeriesData = []
      this.panels.forEach(panel => {
        var seriesData = []
        panel.forEach(seriesid => {
          var s1 = this.series.find(elem => elem.id === seriesid)
          seriesData.push({
            name: s1.name,
            data: s1.data,
            id: s1.id,
            color: s1.color,
            visible: s1.visible,
            lineWidth: this.lineWidth,
            states: {
               hover: {
                  lineWidth: this.lineWidth
               },          
            },
          })
        })
        allSeriesData.push(seriesData)
      })
      return allSeriesData 
    },


    axisOptions() {
      let axes = []
      let axisHeightPercent = Math.floor(100 / this.numAxes)
      let remainder = 100 % this.numAxes
      for (var i = 0; i < this.numAxes; i++) {
        axes.push({
          title: '',
          gridLineWidth: 1, 
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
          animation: false, 
          showAxes: false,
          spacingLeft: this.marginLeft,   
          spacingTop: this.marginTop,
          spacingBottom: this.marginBottom,
        }, 
        plotOptions: {
          series: {
            animation: false,
            lineWidth: this.lineWidth,
            states: {
               hover: {
                  lineWidth: this.lineWidth
               },          
            },
          }
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
          valueDecimals: 0,
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
          gridLineWidth: 0, 
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

.fill-height-or-more {
  display: flex;
  flex-direction: column;
}

.fill-height-or-more > * {
  flex: 1;
}


</style>