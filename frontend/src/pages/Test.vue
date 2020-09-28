<template>

<section class="section is-fullheight">

  <div class="rows">

    <div class="columns">
      <div class="column is-3">
        Actual
      </div>
      <div class="column">
        <AnalysisChart 
          :seriesData="chartsData.series"
          :baseline="chartsData.baseline"
          :anomalies="expectedAnomalies" />
      </div>
    </div>

    <div class="columns"> 
      <div class="column is-3">
        Expected
      </div>
      <div class="column">
        <AnalysisChart
          :seriesData="chartsData.series"
          :anomalies="actualAnomalies" />
      </div>
    </div>

    <div class="columns"> 
      <div class="column is-3">
        Metrics
      </div>
      <div class="column">
        <AnalysisChart
          :seriesData="chartsData.series" />
      </div>
    </div>
  </div>

</section>

</template>



<script>
import AnalysisChart from '../components/AnalysisChart.vue';
import api from "../api/repository";


export default {
  components: { AnalysisChart },
  data() {
    return {
      chartsData: {
        series: [],
        actual: [],
        expected: [],
        baseline: [],
      }
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
.is-fullheight {
  height: calc(100vh - 8.5rem );
  min-height: calc(100vh - 8.5rem);
}

.is-third-height {
  height: 33vh;
}

.rows {
    display: flex;
    flex-direction: column;
}
</style>