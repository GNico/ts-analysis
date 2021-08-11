<template>
<div>
  <div class="is-flex is-justify-content-space-between">
    <div><strong class="has-text-grey-light"> Anomalies histogram </strong></div>
    <b-dropdown  class="header-item" aria-role="list" v-model="selectedBucket">
      <template #trigger>
        <a class="is-flex is-align-items-center has-text-grey">
          <span>Group by: {{selectedBucket.name}}</span>
          <b-icon icon="menu-down"></b-icon>
        </a>
      </template>
      <b-dropdown-item v-for="option in bucketDefs" 
        :value="option" :key="option.name">{{option.name}}</b-dropdown-item>      
    </b-dropdown>
  </div>
  <highcharts 
    :options="histogramChartOptions" 
    :deepCopyOnUpdate="false"/>
</div>
</template>


<script>
const countByFixedStep = function (anomalies, counter, stepInSeconds, indexFunc) {
  var counts = [ ...counter ]
  for (let i=0; i < anomalies.length; i++) {
    var anom = anomalies[i]
    var next = new Date(anom.from) 
    var acc = 0
    while (acc < anom.duration) {
      acc += stepInSeconds
      counts[indexFunc(next)] += 1
      next = new Date(stepInSeconds * 1000 + next.getTime())
    }
  }
  return counts
}

const bucketDefinitions = [
  {
    name: 'Hour',
    counter: new Array(24).fill(0),
    categories: [ ...Array(24).keys() ],
    indexFunc: d => d.getHours(),
    getCounts: function (anomalies) {
      return countByFixedStep(anomalies, this.counter, 3600, this.indexFunc)
    }
  },
  {
    name: 'Day of Week',
    counter:  new Array(7).fill(0),
    categories: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
    indexFunc: d => d.getDay(),
    getCounts: function (anomalies) {
      return countByFixedStep(anomalies, this.counter, 3600 * 24, this.indexFunc)
    }
  },
  {
    name: 'Day of Month',
    counter:  new Array(31).fill(0),
    categories:  Array.from({length: 31}, (_, i) => i + 1),
    indexFunc: d => d.getDate()-1,
    getCounts: function (anomalies) {
      return countByFixedStep(anomalies, this.counter, 3600 * 24, this.indexFunc)      
    }
  },
  {
    name: 'Month',
    counter:  new Array(12).fill(0),
    categories:  ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec'],
    indexFunc: d => d.getMonth(),
    getCounts: function (anomalies) {
      //note: this is not perfectly accurate because months are not all 30 days
      return countByFixedStep(anomalies, this.counter, 3600 * 24 * 30, this.indexFunc)      
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
      selectedBucket: bucketDefinitions[0],
      bucketDefs: bucketDefinitions,
    }
  },
  computed: {        
    histogramChartOptions() {
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
          categories: this.selectedBucket.categories
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
          data: this.selectedBucket.getCounts(this.anomalies),        
        }],
      }
    },
  },
  methods: {    
  }
}

</script>