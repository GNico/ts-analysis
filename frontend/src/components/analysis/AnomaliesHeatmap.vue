<template>
<div>
  <div> <strong class="has-text-grey-light">Anomalies heatmap</strong></div>
  <highcharts 
    :options="heatMapChartOptions" 
    :deepCopyOnUpdate="false"/>
</div>
</template>


<script>

function getPointCategoryName(point, dimension) {
  var series = point.series,
    isY = dimension === 'y',
    axis = series[isY ? 'yAxis' : 'xAxis'];
  return axis.categories[point[isY ? 'y' : 'x']];
}

export default {
  props: {
    anomalies: {
      type: Array,
      default: () => []
    },
  },
  data() {
    return {
    }
  },
  computed: {    
    weeklyMap() {
      var map = new Array(168)
      var dayCounter = 0
      var hourCounter = 0
      for (let i=0; i < 168; i++) {
        map[i] = [ hourCounter, dayCounter, 0]
        dayCounter++
        if (dayCounter > 6) {
          dayCounter = 0
          hourCounter++
        }
      }      
      for (let j=0; j < this.anomalies.length; j++) {
        var start = new Date(this.anomalies[j].from)
        const day = start.getDay()
        const hour = start.getHours()
        const index = hour * 7 + day
        map[index][2] += 1
      } 
      return map
    },
    heatMapChartOptions() {
      return {
        chart: {
          type: 'heatmap',
          height: 250,
          backgroundColor: 'transparent'
        },
        title: {
          text: ''
        },
        xAxis: {
          categories: [ ...Array(24).keys() ]
        },
        yAxis: {
          categories:  ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
          title: null,
          reversed: true
        },
        colorAxis: {
          min: 0,
          gridLineWidth: 1,
          minColor: 'rgba(43, 144, 143,0)',
          maxColor: 'rgba(43, 144, 143,1)'
        },
        credits: false,
        legend: {
          enabled: false,
        }, 
        tooltip: {
          formatter: function() {
            var hour = getPointCategoryName(this.point, 'x')
            var day = getPointCategoryName(this.point, 'y')
            return '<b>' + this.point.value + '</b> anomalies on <b>' + day +
              ', <b> ' + hour + ':00 to ' + hour + ':59 </b>'
          }
        },
        series: [{
          name: 'Weekly distribution',
          borderWidth: 1,
          data: this.weeklyMap,           
          dataLabels: {
            enabled: false,           
          }
        }],
      }
    },   
  },
  methods: {    
  }
}

</script>