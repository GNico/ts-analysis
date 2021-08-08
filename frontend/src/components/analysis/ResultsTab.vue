<template>
<div>
  <div v-if="loading" class="is-size-5 has-text-centered"><i class="mdi mdi-loading icn-spinner"></i> Performing analysis</div>

  <template v-else>
    <div v-if="error" class="is-size-7 error-text"><b-icon type="is-danger" icon="alert" size="is-small"/> {{error}}</div>
    <div v-else class="columns is-fullheight">
      <div class="column is-4 side-menu is-hidden-mobile">        
        <div class="table-header has-text-white">
          <div> <strong class="has-text-white"> Anomalies</strong></div>
          <AnomaliesFilters v-bind="activeOptions" @update="updateOptions"/> 
        </div>

        <AnomaliesTable        
          :anomalies="tableFilteredAnomalies"
          :activeAnomaly="activeAnomaly"
          @changeActive="updateOptions({activeAnomalyId: $event})"/> 
      </div>

      <div class="column main-content">
        <Chart       
          height="400px"
          :seriesData="seriesData"
          :anomalies="chartFilteredAnomalies"
          :loading="loading"
          :activeAnomaly="activeAnomaly"
          :showMinMax="activeOptions.showMinMax"
          :axisInterval="activeOptions.axisInterval"
          @changeActive="updateOptions({activeAnomalyId: $event})"
          @updateRange="updateOptions({selectedRange: { start: $event.start, end: $event.end}})" />

 
        <Subcharts class="mt-3" :anomalies="tableFilteredAnomalies"/> 

      </div>
    </div>  
  </template>
</div>
</template>


<script>
import Chart from './Chart.vue';
import AnomaliesTable from './AnomaliesTable.vue';
import AnomaliesFilters from './AnomaliesFilters.vue'
import debounce from "lodash/debounce";
import Subcharts from "./Subcharts"

export default {
    components: { Chart, AnomaliesTable, AnomaliesFilters, Subcharts },
    data() {
      return {
        polling: null,
      }       
    },
    computed: {
      activeResults() {
        return this.$store.getters['results/activeResults']
      },
      activeOptions() {
        return this.$store.getters['results/activeOptions']
      },
      activeAnomaly() {
        return this.activeOptions.activeAnomalyId
      },
      loading() {
        return this.activeResults.loading
      },
      error() {
        return this.activeResults.error
      },
      resultsData() {
        return this.activeResults.results
      },      
      seriesData() {
        return !this.loading && 
              this.resultsData && 
              this.resultsData.hasOwnProperty("series") && 
              this.activeOptions.showSeries ? this.resultsData.series :  [] 
      },      
      anomalies() {
        return !this.loading &&
              this.resultsData &&      
              this.resultsData.hasOwnProperty("anomalies") ? this.resultsData.anomalies : []
      },
      chartFilteredAnomalies() {
        return this.anomalies.filter(elem => 
          (elem.score >= this.activeOptions.scoreThreshold 
          && (parseInt(elem.to) - parseInt(elem.from) >= this.activeOptions.minDurationTime)))         
      },
      tableFilteredAnomalies() {
        return this.chartFilteredAnomalies.filter(elem =>           
          (!this.activeOptions.selectedRange.start || parseInt(elem.from) > this.activeOptions.selectedRange.start)
          && (!this.activeOptions.selectedRange.end || parseInt(elem.from) < this.activeOptions.selectedRange.end))
      },  
    },
    methods: {
      updateOptions(options) {
        this.$store.dispatch('results/updateOptions', {id: this.activeResults.id, ...options })
      },      
      startPollingResults() {
        this.polling = setInterval(() => {
          console.log('polling results')
          this.$store.dispatch('results/fetchResults', this.activeResults.id)          
        }, 2000)
      },
      stopPollingResults() {
        if (this.polling) {
          console.log('stop polling results')
          clearInterval(this.polling)
        }
        this.polling = null
      }
    },  
    watch: {
      loading: {
        immediate: true,
        handler(val) {
          if (val) {
            this.startPollingResults()
          } else {
            this.stopPollingResults()
          }
        }
      }
    }, 
    beforeDestroy() {
      this.stopPollingResults()
    },  

}
</script>


<style scoped>
.is-fullheight {
  max-height: calc(100vh - 3.5rem);
}
  
.side-menu {
  height: calc(100vh - 17rem);
}

.main-content {
  display: flex;
  flex-direction: column;
  overflow-y: overlay;
  overflow-x: hidden;
}

.table-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
  align-items: center;
}

.error-text {
  white-space: pre;
  font-family: monospace;
}


</style>