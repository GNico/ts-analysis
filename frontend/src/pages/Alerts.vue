<template>
<div>
  <section>
  
        <button class="button is-primary is-medium"
            @click="isModalActive = true">
            Open
        </button>


        <b-modal 
        :active.sync="isModalActive" 
        has-modal-card 
        :can-cancel="['escape', 'outside']" 
        animation='' 
        scroll='keep'>
           
          <div class="modal-card">
            <header class="modal-card-head">
              <p class="modal-card-title">Options</p>
            </header>

            <section class="modal-card-body">
              HELLO
            </section>

          </div>
        </b-modal>
  </section>

<highcharts class="chart" :constructor-type="'stockChart'" :options="chartOptions" :updateArgs="updateArgs" ref="chart"></highcharts>

</div>
</template>


<script>


export default {

  data () {
    return {
      isModalActive: false,
      updateArgs: [true, true, {duration: 1000}],
      chartOptions: {
        chart: {
          zoomType: 'x',
          panning: true,
          panKey: 'shift',
          backgroundColor: "#073642",
          height: '700',
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
          enabled: true,
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

        /* [{
          title: '',
          // settings for multiple panes in the chart
          height: '33%',
          top: '0%',
          offset: false,
          resize: {
            enabled: true,
            lineWidth: 2,
          }
        },
        {
          title: '',
          // settings for multiple panes in the chart
          height: '33%',
          top: '33%',
          offset: false,
          resize: {
            enabled: true,
            lineWidth: 2,
          }
        },
        {
          title: '',
          // settings for multiple panes in the chart
          height: '33%',
          top: '66%',
          offset: false,          
        }], */
        series: [ {
          name: 'Pepega',
          data: [43934, 52503, 57177, 69658, 97031, 119931, 137133, 154175, 43934, 52503, 57177, 69658, 97031, 119931, 137133, 154175],
          yAxis: 0
        },
        {
          name: 'Other',
          data:  [24916, 24064, 29742, 29851, 32490, 30282, 38121, 40434, 24916, 24064, 29742, 29851, 32490, 30282, 38121, 40434],
          yAxis: 1
        },
        {
          name: 'Third',
          data: [11744, 17722, 16005, 19771, 20185, 24377, 32147, 39387, 11744, 17722, 16005, 19771, 20185, 24377, 32147, 39387],
          yAxis: 2
        }, ]
      }
    }
  },
  methods: {
    calcAxis(numAxes) {
      let axisHeightPercent = Math.floor(100 / numAxes)
      let remainder = 100 % numAxes
      console.log(remainder)

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


<style>


</style>