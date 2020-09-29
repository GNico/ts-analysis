<template>


  <div class="rows">

    <div class="columns">
      <div class="column is-3">
        Actual
      </div>
      <div class="column">
        <AnalysisChart 

          :seriesData="chartsData.series"
          :baseline="chartsData.baseline"
          :anomalies="expectedAnomalies" 
          :extremes="extremes"
          @changedExtremes="syncExtremes"/>
      </div>
    </div>

    <div class="columns"> 
      <div class="column is-3">

        <div class="columns">
          <div class="column is-6">
            <div class="notification tp">True positives: {{ chartsData.metrics.tp }}</div>
          </div>
          <div class="column is-6">
            <div class="notification is-primary">False positives: {{ chartsData.metrics.fp }}</div>
          </div>
        </div>
        <div class="columns">
          <div class="column is-6">
            <div class="notification is-primary">False negatives: {{ chartsData.metrics.fn }}</div>
          </div>
          <div class="column is-6">
            <div class="notification is-primary">True negatives: {{ chartsData.metrics.tn }}</div>
          </div>
        </div>        
      </div>
      <div class="column">
        <TestMetricsChart
          :seriesData="chartsData.series"
          :anomalies="actualAnomalies"
          :extremes="extremes"
          :metrics="chartsData.metrics.values"
          @changedExtremes="syncExtremes" />
      </div>
    </div>  

  </div>


</template>



<script>
import AnalysisChart from '../components/AnalysisChart.vue';
import TestMetricsChart from '../components/TestMetricsChart.vue';
import api from "../api/repository";


export default {
  components: { AnalysisChart, TestMetricsChart },
  data() {
    return {

      chartsData: {
        series: [],
        actual: [],
        expected: [],
        baseline: [],
        metrics: {},
      },
      extremes: {
        min: undefined,
        max: undefined,
      },
    }
  },
  computed: {
    expectedAnomalies() {
      var anoms = []
      var idx = 0
      for (var item of this.chartsData.expected) {
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
    actualAnomalies() {
      var anoms = []
      var idx = 0
      for (var item of this.chartsData.actual) {
          anoms.push({
                  id: idx.toString(),
                  from: item.from,
                  to: item.to,
                  score: item.score,
              })
          idx++
      }
      return anoms
    }

  },
  methods: {
    syncExtremes(event) {
      this.extremes = { min: event.min, max: event.max }
    
    }
  },
  mounted: function () {
    api.testAlgo()
      .then(response => {       
        this.chartsData = { ...response.data }
      })
      .catch(error => { 
        console.log('error analizing data')
        console.log(error)
      })
  }

}

</script>



<style scoped>

.tp {
  background-color: red;
}

.is-fullheight {
  height: calc(100vh - 8.5rem );
  min-height: calc(100vh - 8.5rem);
}

.rows {
    display: flex;
    flex-direction: column;
}

.chch {
  height: 30vh;
}

</style>