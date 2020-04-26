<template>
<div class="chart-container columns is-gapless is-multiline" >   
  <div class="column is-1 char-sec">
    <div class="legends">
      <LegendSeriesTag color="red">Peeee pepepe </LegendSeriesTag>
      <LegendSeriesTag color="blue">Second series </LegendSeriesTag>     
    </div>
  </div>
  <div class="column is-offset-1 is-11 char-sec chart" >
    <highcharts class="chart" :constructor-type="'stockChart'" :options="chartOptions" :updateArgs="updateArgs" ref="chart"></highcharts>
  </div>
</div>
</template>


<script>

import LegendSeriesTag from '../components/LegendSeriesTag.vue';

export default {
  components: { LegendSeriesTag },
  data () {
    return {
      updateArgs: [true, true, {duration: 1000}],
      chartOptions: {
        chart: {
          zoomType: 'x',
          panning: true,
          panKey: 'shift',
          backgroundColor: "#073642",
          //height: '700',
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
        },   
        yAxis: this.calcAxis(3),
        series: [ {
          name: 'Pepega',
          data: [
          [
              1524058200000,
              177.84
          ],
          [
              1524144600000,
              172.8
          ],
          [
              1524231000000,
              165.72
          ],
          [
              1524490200000,
              165.24
          ],
          [
              1524576600000,
              162.94
          ]],
          yAxis: 0,
        },
        {
          name: 'Other',
          data:  [
          [
              1524058200000,
              176.57
          ],
          [
              1524144600000,
              176.89
          ],
          [
              1524231000000,
              183.83
          ],
          [
              1524490200000,
              185.16
          ],
          [
              1524576600000,
              186.05
          ]],
          yAxis: 1,
        },
        {
          name: 'Third',
          data: [
          [
              1524058200000,
              163.65
          ],          
          [
              1524144600000,
              164.22
          ],
          [
              1524231000000,
              162.32
          ],
          [
              1524490200000,
              165.26
          ],
          [
              1524576600000,
              169.1
          ]],
          yAxis: 2,
        }] 
      }
    }
  },
  methods: {    
    calcAxis(numAxes) {
      let axisHeightPercent = Math.floor(100 / numAxes)
      let remainder = 100 % numAxes
      let axisOptions = []
      for (var i = 0; i < numAxes; i++) {
        axisOptions.push({
          title: '',
          offset: false,
          opposite: true,
          resize: (i<numAxes-1) ? {
            enabled: true,
            lineColor: 'gray',
            lineWidth: 2,
          } : undefined,
          crosshair: {
            snap: false,
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
          height: i==numAxes-1 ? '' + (axisHeightPercent + remainder) + '%' : '' + axisHeightPercent + '%' ,
          top: '' + (i * axisHeightPercent) + '%',    
        })
      }
      return axisOptions
    },
  }
}


</script>



<style scoped>

.chart-container { 
  position: relative;
 }

.char-sec {
  background-color: #073642;
  height: inherit;
}

.legends {
  position: absolute;
  z-index: 99999;
}

.chart {
  height: inherit;
}

</style>