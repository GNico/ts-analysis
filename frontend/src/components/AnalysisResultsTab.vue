<template>
  <div v-if="loading"> Retrieving analysis results... </div>
  <div v-else class="columns is-fullheight">
    <div class="column is-4 side-menu is-hidden-mobile">        
      <div class="table-header has-text-white">
        <div> <strong class="has-text-grey-light" > <i> {{ sidebarTitle }} </i></strong></div>
        <a class="button is-info is-small" @click="toggleFilters" :class="{ 'is-outlined': !showFiltersMenu }">
        <span class="icon"><i :class="showFiltersMenu ? 'mdi mdi-close' : 'mdi mdi-filter-variant'"></i></span>
        <span>Filters</span></a>
      </div>

      <div v-if="showFiltersMenu">
      <!--  <b-field horizontal label="Date range">
          <b-datepicker             
            :first-day-of-week="1"
            placeholder="From"
            size="is-small"
            v-model="selectedRange.start">
            <button class="button is-primary is-small"
              @click="selectedRange.start = new Date()">
              <b-icon  icon="calendar-today" size="is-small"></b-icon>
              <span>Today</span>
            </button>
            <button class="button is-danger is-small"
              @click="selectedRange.start = null">
              <b-icon icon="close-thick" size="is-small"></b-icon>
              <span>Clear</span>
            </button>
          </b-datepicker>

          <b-datepicker             
            :first-day-of-week="1"
            placeholder="To"
            size="is-small"
            v-model="selectedRange.end">
            <button class="button is-primary is-small"
              @click="selectedRange.end = new Date()">
              <b-icon  icon="calendar-today" size="is-small"></b-icon>
              <span>Today</span>
            </button>
            <button class="button is-danger is-small"
              @click="selectedRange.end = null">
              <b-icon icon="close-thick" size="is-small"></b-icon>
              <span>Clear</span>
            </button>
          </b-datepicker>
        </b-field>  

      -->

        <b-field horizontal label="Min Duration">
          <b-tooltip
            label="Input must be a number followed by a valid letter [ m = minutes, h = hour, d = day ]"
            size="is-large"
            position="is-bottom"
            multilined>
            <b-input v-model="minDuration" @input="checkValid" ref="regexinput" type="text" pattern="^[0-9]+[mhd]$" size="is-small" expanded/>
          </b-tooltip> 
        </b-field>

        <b-field horizontal label="Score threshold">
          <b-slider v-model="scoreThreshold" lazy indicator></b-slider>
        </b-field>

        <b-field horizontal label="">
          <b-checkbox v-model="showSeries">
            <strong class="has-text-white">Show series</strong>
          </b-checkbox>        
        </b-field>
            
        <b-field horizontal label="">
          <b-checkbox v-model="showBaseline">
            <strong class="has-text-white">Show baseline</strong>
          </b-checkbox>        
        </b-field>

        <b-field horizontal label="">
          <b-checkbox v-model="showTrend">
            <strong class="has-text-white">Show trend</strong>
          </b-checkbox>        
        </b-field>
      </div>

      <AnalysisAnomaliesTable 
        v-else
        id="anom-table"
        :anomalies="filteredAnomalies"
        :activeAnomaly="filteredActiveAnomaly"
        @changeActive="setActiveAnomaly"/> 
    </div>

    <div class="column main-content">
      <AnalysisChart       
        :seriesData="seriesData"
        :baseline="baseline"
        :anomalies="filteredAnomalies"
        :loading="loading"
        :activeAnomaly="filteredActiveAnomaly"
        @changeActive="setActiveAnomaly"
        @updateRange="updateRange" />

        <!--  :range="selectedRangeTimestamp" -->
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
        showSeries: true,
        showTrend: false,
        scoreThreshold: 0,
        minDuration: '',
        minDurationTime: 0,
        selectedRange: {
          start: null,
          end: null
        },
      }       
    },
    computed: {
      id() {
        return this.$store.state.analysis.activeAnalysisId
      },
      activeAnomaly() {
        return this.$store.state.analysis.activeAnomalyId
      },
      results() {
        return this.$store.getters['analysis/getResultsById'](this.id) 
      },
      loading() {
        return this.results.loading
      },
      seriesData() {
        return !this.loading && this.results.hasOwnProperty("series") && this.showSeries ? this.results.series :  [] 
      },
      baseline() {
        return (!this.loading && this.results.hasOwnProperty("baseline") && this.showBaseline) ? this.results.baseline : []
      },
      anomalies() {
        return !this.loading && this.results.hasOwnProperty("anomalies") ? this.results.anomalies : []
      },
   /*   selectedRangeTimestamp() {
        let start = undefined
        let end = undefined
        if (this.selectedRange.start) 
          start = Math.round(this.selectedRange.start.getTime())
        if (this.selectedRange.end) 
          end = Math.round(this.selectedRange.end.getTime())      
        return {start, end}
      },  */
      filteredAnomalies() {
        return this.anomalies.filter(elem => 
          (elem.score > this.scoreThreshold 
          && (parseInt(elem.to) - parseInt(elem.from) >= this.minDurationTime)
          && (!this.selectedRange.start || parseInt(elem.from) > this.selectedRange.start)
          && (!this.selectedRange.end || parseInt(elem.from) < this.selectedRange.end)))
         // && (!this.selectedRangeTimestamp.start || parseInt(elem.from) > this.selectedRangeTimestamp.start)
         // && (!this.selectedRangeTimestamp.end || parseInt(elem.from) < this.selectedRangeTimestamp.end)))
      },
      filteredActiveAnomaly() {
        let filteredAnom = this.filteredAnomalies.find(elem => elem.id === this.activeAnomaly)
        return filteredAnom ? filteredAnom.id : ''
      },
      activeAnomaly() {
        return this.$store.state.analysis.activeAnomalyId
      },
      sidebarTitle() {
        return this.showFiltersMenu ? 'Filter Options' : 'Anomalies'
      }
    },
    methods: {
      updateRange(event) {    
        // this.selectedRange.start = new Date(event.start)
        // this.selectedRange.end = new Date(event.end)
        this.selectedRange.start = event.start
        this.selectedRange.end = event.end
      },
      setActiveAnomaly(id) {
        this.$store.dispatch('analysis/setActiveAnomaly', id)
      },
      toggleFilters() {
        this.showFiltersMenu = !this.showFiltersMenu
      },
      checkValid() {
        if (!this.minDuration) {
          this.minDurationTime = 0
          return
        }
        if (this.$refs.regexinput.checkHtml5Validity()) {
          let numbers = this.minDuration.match(/\d+/g)
          let letter = this.minDuration.match(/[mhd]/g)
          let ms = 0
          switch (letter[0]) {
            case "m":
              ms = 60000
              break
            case "h":
              ms = 3600000
              break
            case "d": 
              ms = 86400000
              break
            default:
              break
          }
          this.minDurationTime = parseInt(numbers[0]) *  ms 
        }
      }
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

</style>