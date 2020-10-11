<template>
<div class="columns"> 
  <div class="column is-3 fixedsize">
    <b-field grouped group-multiline>
      <div class="control">
          <b-taglist attached>
              <b-tag class="has-background-grey-dark has-text-white">TP</b-tag>
              <b-tag type="is-info">{{ chartData.metrics.tp }}</b-tag>
          </b-taglist>
      </div>

      <div class="control">
          <b-taglist attached>
              <b-tag class="has-background-grey-dark has-text-white">FP</b-tag>
              <b-tag type="is-link">{{ chartData.metrics.fp }}</b-tag>
          </b-taglist>
      </div>

      <div class="control">
          <b-taglist attached>
              <b-tag class="has-background-grey-dark has-text-white">FN</b-tag>
              <b-tag type="is-danger">{{ chartData.metrics.fn }}</b-tag>
          </b-taglist>
      </div>
    </b-field>

    <b-field grouped group-multiline>
      <div class="control">
          <b-taglist attached>
              <b-tag class="has-background-grey-dark has-text-white">Precision</b-tag>
              <b-tag type="is-primary">{{ chartData.metrics.precision }}</b-tag>
          </b-taglist>
      </div>

      <div class="control">
          <b-taglist attached>
              <b-tag class="has-background-grey-dark has-text-white">Recall</b-tag>
              <b-tag type="is-primary">{{ chartData.metrics.recall }}</b-tag>
          </b-taglist>
      </div>          
    </b-field>


    <AnalysisAnomaliesTable
      :anomalies="actualAnomalies"        
      :activeAnomaly="activeAnomaly"
      height=270                       
      @changeActive="setActiveAnomaly" /> 
    <div>
      {{ activeAnomalyInfo }}
    </div>
      

  </div>
  <div class="column">
    <TestMetricsChart
      :seriesData="chartData.series"
      :anomalies="actualAnomalies"
      :baseline="chartData.baseline"
      :extremes="extremes"
      :metrics="chartData.metrics.values"
      :activeAnomaly="activeAnomaly"
      :metricColors="colors"
      @changedExtremes="syncExtremes" 
      @changeActive="setActiveAnomaly"/>
  </div>
</div>  

</template>



<script>
import AnalysisAnomaliesTable from '../components/AnalysisAnomaliesTable.vue';
import TestMetricsChart from '../components/TestMetricsChart.vue';


export default {
  components: { AnalysisAnomaliesTable, TestMetricsChart },
  props: {    
    chartData: {
      type: Object,
      default: () => { 
        return {
          series: [],
          anomalies: [],
          baseline: [],
          metrics: {},
        }
      }
    },
  },
  data() {
    return {
      colors: {
        tp: '#268bd2',
        fp: '#b58900',
        fn: '#d33682',
      },   
      extremes: {
        min: undefined,
        max: undefined,
      },
      activeAnomaly: '',
    }
  },
  computed: {
    actualAnomalies() {
      var anoms = []
      var idx = 0
      for (var item of this.chartData.anomalies) {
          anoms.push({
            id: idx.toString(),
            from: item.from,
            to: item.to,
            score: item.score,
          })
          idx++
      }
      return anoms
    },
    activeAnomalyInfo() {
      return this.actualAnomalies.find(anom => anom.id === this.activeAnomaly)
    },
  },
  methods: {
    syncExtremes(event) {
      this.extremes = { min: event.min, max: event.max }
    },
    setActiveAnomaly(id) {
      this.activeAnomaly = id
    }
  },  

}

</script>



<style scoped>


.fixedsize {
  height: 400px;   
  overflow-y: auto;
}

.outline {
  color: white;
  font-size: 1rem;
  text-shadow: -1px 1px 0 #000,
                1px 1px 0 #000,
                1px -1px 0 #000,
               -1px -1px 0 #000;
}

</style>