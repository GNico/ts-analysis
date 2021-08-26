<template>
<div>
  <div class="is-flex is-justify-content-space-between">
    <div><strong class="has-text-grey-light">Anomalies heatmap</strong></div>
    <b-dropdown  class="header-item" aria-role="list" v-model="selectedBucket">
      <template #trigger>
        <a class="is-flex is-align-items-center has-text-grey">
          <span>{{selectedBucket.name}}</span>
          <b-icon icon="menu-down"></b-icon>
        </a>
      </template>
      <b-dropdown-item v-for="option in bucketDefs" 
        :value="option" :key="option.name">{{option.name}}</b-dropdown-item>      
    </b-dropdown>
  </div>
  <highcharts 
    :options="heatMapChartOptions" 
    :deepCopyOnUpdate="false"/>
</div>
</template>


<script>
//pre: step in seconds correspond to lowest axis increment
const countByFixedStep = function (anomalies, categoriesX, categoriesY, stepInSeconds, indexFuncX, indexFuncY) {
  //init counter
  var counter = []
  for (let i=0; i < categoriesX.length; i++) {
    for (let j=0; j < categoriesY.length; j++) {
      counter.push([i, j, 0]) 
    }
  }
  //count
  for (let k=0; k < anomalies.length; k++) {
    var anom = anomalies[k]
    var next = new Date(anom.from) 
    console.log(next)
    var acc = 0
    while (acc < anom.duration) {
      acc += stepInSeconds
      const index = indexFuncX(next) * categoriesY.length + indexFuncY(next)
      counter[index][2] += 1
      next = new Date(stepInSeconds * 1000 + next.getTime())
    }
  }
  return counter
}


const axisDefinitions = [
  {
    name: 'Hour of day/Day of week',
    categoriesX: [ ...Array(24).keys() ],
    categoriesY: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
    indexFuncX: d => d.getHours(),
    indexFuncY: d => d.getDay(),
    getCounts: function (anomalies) {
      return countByFixedStep(anomalies, this.categoriesX, this.categoriesY, 3600, this.indexFuncX, this.indexFuncY)
    },
    getPointCategoryName: function(point, dimension) {
      const tooltipNamesY = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
      return dimension === 'y' ? 
        tooltipNamesY[point['y']] : 
        this.categoriesX[point['x']] + ':00 to ' + this.categoriesX[point['x']] + ':59'
    } 
  },
  {
    name: 'Day of month/Day of week',
    categoriesX: Array.from({length: 31}, (_, i) => i + 1),
    categoriesY: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
    indexFuncX: d => d.getDate()-1,
    indexFuncY: d => d.getDay(),
    getCounts: function (anomalies) {
      return countByFixedStep(anomalies, this.categoriesX, this.categoriesY, 3600 * 24, this.indexFuncX, this.indexFuncY)
    },
    getPointCategoryName: function(point, dimension) {
      const tooltipNamesY = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
      return dimension === 'y' ? tooltipNamesY[point['y']] : this.categoriesX[point['x']]
    }  
  },
  {
    name: 'Day of month/Month of year',
    categoriesX: Array.from({length: 31}, (_, i) => i + 1),
    categoriesY: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec'],
    indexFuncX: d => d.getDate()-1,
    indexFuncY: d => d.getMonth(),
    getCounts: function (anomalies) {
      return countByFixedStep(anomalies, this.categoriesX, this.categoriesY, 3600 * 24, this.indexFuncX, this.indexFuncY)
    },  
    getPointCategoryName: function(point, dimension) {
      const tooltipNamesY = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
      return dimension === 'y' ? tooltipNamesY[point['y']] : this.categoriesX[point['x']]
    } 
  },
]


export default {
  props: {
    anomalies: {
      type: Array,
      default: () => []
    },
  },
  data() {
    return {
      selectedBucket: axisDefinitions[0],
      bucketDefs: axisDefinitions,
    }
  },
  computed: {    
    heatMapChartOptions() {
      var vm = this
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
          categories: this.selectedBucket.categoriesX,
        },
        yAxis: {
          categories:  this.selectedBucket.categoriesY,
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
            var catx = vm.selectedBucket.getPointCategoryName(this.point, 'x')
            var caty = vm.selectedBucket.getPointCategoryName(this.point, 'y')
            return '<b>' + this.point.value + '</b> anomalies on <b>' + caty +
              ', <b> ' + catx +'</b>'
          }
        },
        series: [{
          name: this.selectedBucket.name,
          borderWidth: 1,
          data: this.selectedBucket.getCounts(this.anomalies),           
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