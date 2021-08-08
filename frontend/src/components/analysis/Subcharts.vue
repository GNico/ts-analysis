<template>
<div class="columns">
  <div class="column is-5">
    <div class="is-flex is-justify-content-space-between">
      <div><strong class="has-text-grey-light"> Date histogram </strong></div>
      <b-dropdown  class="header-item" aria-role="list" v-model="selectedBucket">
        <template #trigger>
          <a class="is-flex is-align-items-center has-text-grey">
            <span>Group by: {{selectedBucket}}</span>
            <b-icon icon="menu-down"></b-icon>
          </a>
        </template>
        <b-dropdown-item v-for="option in histogramBucketOptions" 
          :value="option" :key="option">{{option}}</b-dropdown-item>      
      </b-dropdown>
    
    </div>
    <highcharts 
      :options="histogramOptions" 
      :deepCopyOnUpdate="false"/>
  </div>
  <div class="column is-7">
    <div> <strong class="has-text-grey-light">Weekly distribution </strong></div>
    <highcharts 
      :options="heatMapChartOptions" 
      :deepCopyOnUpdate="false"/>
  </div>  
</div>
</template>


<script>
import Highcharts from 'highcharts'

const allHours =  [ ...Array(24).keys() ]
const allMonths = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
const allWeekdays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
const allWeekdaysShort = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

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
    }
  },
  data() {
    return {
      histogramBucketOptions: [ 'Hour', 'Day', 'Month'],
      selectedBucket: 'Day'
    }
  },
  computed: {
    histogramData() {
      var groups = {
        months: new Array(12).fill(0),
        days: new Array(7).fill(0),
        hours: new Array(24).fill(0)
      }
      for (let i=0; i < this.anomalies.length; i++) {
        var start = new Date(this.anomalies[i].from)
        const hour = start.getHours()
        const day = start.getDay()
        const month = start.getMonth()
        groups.months[month] += 1
        groups.days[day] += 1
        groups.hours[hour] += 1
      }
      return groups

    },
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
         /* title: {
              enabled: true,
              text: 'hours'
          },*/
          categories: [ ...Array(24).keys() ]
        },
        yAxis: {
          categories: allWeekdays,
          title: null,
          reversed: true
        },
        colorAxis: {
          min: 0,
          gridLineWidth: 1,
         // minColor: '#FFFFFF',
         // maxColor: Highcharts.getOptions().colors[0]
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
            enabled: true,
            color: '#000000',
            filter: {
              property: 'value',
              operator: '>',
              value: 0
            }
          }
        }],
      }
    },
    bucketOptions() {
      switch (this.selectedBucket) {
        case 'Hour':
          return {
            categories: allHours,
            data: this.histogramData.hours
          }
        case 'Day':
          return {
            categories: allWeekdaysShort,
            data: this.histogramData.days
          }
        case 'Month':
          return {
            categories: allMonths,
            data: this.histogramData.months
          }  
        default:
          return {}
      }
    },
    histogramOptions() {
      return {
        chart: {
          type: 'column',
          height: 250,
          backgroundColor: 'transparent'
        },
        title: {
          text: ''
        },
        xAxis: {        
          categories: this.bucketOptions.categories
        },
        yAxis: {
          title: null,
        },        
        credits: false,  
        legend: {
          enabled: false,
        }, 
        plotOptions: {
          column: {
            pointPadding: 0,
            borderWidth: 0,
            groupPadding: 0,
            shadow: false
          }
        },
        series: [{
          name: 'Total anomalies',
          borderWidth: 1,
          data: this.bucketOptions.data,        
        }],
      }
    },
  },
  methods: {    
  }
}

</script>