<template>

  <div class="columns is-fullheight">

    <div class="column is-4 side-menu is-hidden-mobile">        
      <div class="table-header has-text-white">
        <div> <strong class="has-text-white" v-show="!showFiltersMenu"> Anomalies </strong></div>
        <a class="button is-info is-small" @click="toggleFilters" :class="{ 'is-outlined': !showFiltersMenu }">
        <span class="icon"><i :class="showFiltersMenu ? 'mdi mdi-close' : 'mdi mdi-filter-variant'"></i></span>
        <span>Filters</span></a>
      </div>

      <div v-if="showFiltersMenu">
        <b-field label="Score threshold">
            <b-slider v-model="scoreThreshold" lazy indicator></b-slider>
        </b-field>

        <div class="field">
            <b-checkbox v-model="showBaseline">
                <strong class="has-text-white">Show baseline</strong>
            </b-checkbox>
        </div>

      </div>

      <AnalysisAnomaliesTable 
        v-else
        :anomalies="filteredAnomalies"
        :activeAnomaly="activeAnomaly"
        @changeActive="setActiveAnomaly"/> 
    </div>

    <div class="column main-content">
      <AnalysisChart 
        :seriesData="seriesData"
        :baseline="baseline"
        :anomalies="filteredAnomalies"
        :loading="loading"
        :activeAnomaly="activeAnomaly"
        @changeActive="setActiveAnomaly"/>

      
    </div>

  </div>  

</template>


<script>
import AnalysisChart from '../components/AnalysisChart.vue';
import AnalysisSettings from '../components/AnalysisSettings.vue';
import AnalysisAnomaliesTable from '../components/AnalysisAnomaliesTable.vue';


export default {
    components: { AnalysisChart, AnalysisSettings, AnalysisAnomaliesTable },
    data() {
      return {
        showFiltersMenu: false,
        showBaseline: true,
        scoreThreshold: 0,
      }       
    },
    computed: {
      id() {
        return this.$store.state.analysis.activeAnalysisId
      },
      results() {
        return this.$store.getters['analysis/getResultsById'](this.id) 
      },
      loading() {
        return this.results.loading
      },
      seriesData() {
        return !this.loading && this.results.hasOwnProperty("series") ? this.results.series :  [] 
      },
      baseline() {
        return (!this.loading && this.results.hasOwnProperty("baseline") && this.showBaseline) ? this.results.baseline : []
      },
      anomalies() {
        return !this.loading && this.results.hasOwnProperty("anomalies") ? this.results.anomalies : []
      },
      filteredAnomalies() {
        let filtered = []
        this.anomalies.forEach(elem => {
          if (elem.score > this.scoreThreshold)
            filtered.push(elem)
        })
        return filtered
      },
      activeAnomaly() {
        return this.$store.state.analysis.activeAnomalyId
      }
    },
    methods: {
      setActiveAnomaly(id) {
        this.$store.dispatch('analysis/setActiveAnomaly', id)
      },
      toggleFilters() {
        this.showFiltersMenu = !this.showFiltersMenu
      }
    },
    watch: {

    }
}

</script>



<style scoped>


.is-fullheight {
  max-height: calc(100vh - 3.5rem);
}
  
.side-menu {
  overflow-y: auto;
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
</style>