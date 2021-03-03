<template>

<div v-else class="columns" :style="{height: height + 50 + 'px'}">
  <div class="column main-content" :style="{height: height + 'px'}">
    <div class="section-header has-text-white">
      <slot> </slot>
    </div>

    <Chart     
      class="thechart"
      :seriesData="series"
      :baseline="baseline"
      :anomalies="filteredAnomalies"
      :loading="loading"
      :activeAnomaly="filteredActiveAnomaly"
      :range="extremes"
      @changeActive="activeAnomalyId = $event"
      @updateRange="updateRange" />
  </div>

  <div class="column is-4" :style="{height: height + 'px'}">     
    <template v-if="anomalies.length">
      <div class="section-header has-text-white">
        <div> <strong class="has-text-grey-light" > <i> Anomalies </i></strong></div>
        <AnomaliesFilters v-bind="filters" @update="updateOptions"/> 
      </div>

      <AnomaliesTable   
        id="anom-table"
        :anomalies="filteredAnomalies"
        :activeAnomaly="filteredActiveAnomaly"
        @changeActive="activeAnomalyId = $event"
        /> 
    </template>
  </div>
</div> 
  

</template>

<script>
import AnomaliesTable from './AnomaliesTable'
import AnomaliesFilters from './AnomaliesFilters'
import Chart from './Chart'

export default {
  components: { AnomaliesTable, AnomaliesFilters, Chart },
  props: {
    series: {
      type: Array,
      default: () => []
    },
    anomalies: {
      type: Array,
      default: () => []
    },
    baseline: {
      type: Array,
      default: () => []
    },
    height: {
      type: Number,
      default: 400,
    },
    extremes: {
      type: Object,
      default: () => {return {}}
    }
  },
  data () {
    return {
      loading: false,
      activeAnomalyId: '',
      filters: {
        showBaseline: true,
        showSeries: true,
        showTrend: false,
        scoreThreshold: 0,
        minDuration: '',
        minDurationTime: 0,
        selectedRange: {
          start: null,
          end: null
        }
      }    
    }
  },
  computed: {
    filteredAnomalies() {
      return this.anomalies.filter(elem => 
        (elem.score > this.filters.scoreThreshold 
        && (parseInt(elem.to) - parseInt(elem.from) >= this.filters.minDurationTime)
        && (!this.filters.selectedRange.start || parseInt(elem.from) > this.filters.selectedRange.start)
        && (!this.filters.selectedRange.end || parseInt(elem.from) < this.filters.selectedRange.end)))
    },
    filteredActiveAnomaly() {
      let filteredAnom = this.filteredAnomalies.find(elem => elem.id === this.activeAnomalyId)
      return filteredAnom ? filteredAnom.id : ''
    },
  },
  methods: {
    updateRange(event) {
      this.$emit('updateRange', event)
      console.log(event)
    },
    updateOptions() {
      
    }
  }
}
</script>



<style scoped>
/*.main-content {
  display: flex;
  flex-direction: column;
  overflow-y: overlay;
  overflow-x: hidden;
} */

.thechart {
  height: inherit;
}

.section-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
  align-items: center;
  height: 30px;
}

</style>