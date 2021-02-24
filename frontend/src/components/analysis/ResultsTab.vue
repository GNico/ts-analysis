<template>
<div>
  <div v-if="loading" class="is-size-5 has-text-centered"><i :class="loading ?  'mdi mdi-loading icn-spinner' : ''"></i> Performing analysis</div>
  <div v-else class="columns is-fullheight">
    <div class="column is-4 side-menu is-hidden-mobile">        
      <div class="table-header has-text-white">
        <div> <strong class="has-text-grey-light" > <i> {{ sidebarTitle }} </i></strong></div>
        <a class="button is-info is-small" @click="toggleFilters" :class="{ 'is-outlined': !showFiltersMenu }">
        <span class="icon"><i :class="showFiltersMenu ? 'mdi mdi-close' : 'mdi mdi-filter-variant'"></i></span>
        <span>Filters</span></a>
      </div>

      <div v-if="showFiltersMenu">
     <!--   <b-field horizontal label="Min Duration">
          <b-tooltip
            label="Input must be a number followed by a valid letter [ m = minutes, h = hour, d = day ]"
            size="is-large"
            position="is-bottom"
            multilined>
            <b-input 
              v-model="minDuration" 
              @input="checkValid" 
              ref="regexinput" 
              type="text" 
              pattern="^[0-9]+[mhd]$" 
              size="is-small" 
              expanded
              icon-right="close-circle"
              icon-right-clickable
              @icon-right-click="minDuration = ''"/>
          </b-tooltip> 
        </b-field> -->

        <b-field horizontal label="Score threshold" >
          <b-slider :value="activeOptions.scoreThreshold" @input="updateOptions('scoreThreshold', $event)" lazy indicator></b-slider>
        </b-field>


        <b-field horizontal label="">
          <b-checkbox :value="activeOptions.showSeries" @input="updateOptions('showSeries', $event)">
            <strong class="has-text-white">Show series</strong>
          </b-checkbox>        
        </b-field>
            
        <b-field horizontal label="">
          <b-checkbox :value="activeOptions.showBaseline" @input="updateOptions('showBaseline', $event)">
            <strong class="has-text-white">Show baseline</strong>
          </b-checkbox>        
        </b-field>

        <b-field horizontal label="">
          <b-checkbox :value="activeOptions.showTrend" @input="updateOptions('showTrend', $event)">
            <strong class="has-text-white">Show trend</strong>
          </b-checkbox>        
        </b-field>
      </div>

      <AnomaliesTable
        v-else
        id="anom-table"
        :anomalies="filteredAnomalies"
        :activeAnomaly="filteredActiveAnomaly"
        @changeActive="updateOptions('activeAnomalyId', $event)"
        /> 
    </div>

    <div class="column main-content">
      <Chart       
        :seriesData="seriesData"
        :baseline="baseline"
        :anomalies="filteredAnomalies"
        :loading="loading"
        :activeAnomaly="filteredActiveAnomaly"
        @changeActive="updateOptions('activeAnomalyId', $event)"
        @updateRange="updateOptions('selectedRange', $event)" />
    </div>
  </div>  
</div>
</template>


<script>
import Chart from './Chart.vue';
import AnomaliesTable from './AnomaliesTable.vue';

export default {
    components: { Chart, AnomaliesTable },
    data() {
      return {
        showFiltersMenu: false,
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
      resultsData() {
        return this.activeResults.results
      },      
      seriesData() {
        return !this.loading && 
              this.resultsData && 
              this.resultsData.hasOwnProperty("series") && 
              this.activeOptions.showSeries ? this.resultsData.series :  [] 
      },
      baseline() {
        return (!this.loading && 
              this.resultsData &&
              this.resultsData.hasOwnProperty("baseline") && 
              this.showBaseline) ? this.resultsData.baseline : []
      },
      anomalies() {
        return !this.loading &&
              this.resultsData &&      
              this.resultsData.hasOwnProperty("anomalies") ? this.resultsData.anomalies : []
      },
      filteredAnomalies() {
        return this.anomalies.filter(elem => 
          (elem.score > this.activeOptions.scoreThreshold 
          && (parseInt(elem.to) - parseInt(elem.from) >= this.activeOptions.minDurationTime)
          && (!this.activeOptions.selectedRange.start || parseInt(elem.from) > this.activeOptions.selectedRange.start)
          && (!this.activeOptions.selectedRange.end || parseInt(elem.from) < this.activeOptions.selectedRange.end)))
      },
      filteredActiveAnomaly() {
        let filteredAnom = this.filteredAnomalies.find(elem => elem.id === this.activeAnomaly)
        return filteredAnom ? filteredAnom.id : ''
      },
      sidebarTitle() {
        return this.showFiltersMenu ? 'Filter Options' : 'Anomalies'
      }
    },
    methods: {
      updateOptions(prop, value) {
        this.$store.dispatch('results/updateOptions', {id: this.activeResults.id, [prop]: value })
      },
      toggleFilters() {
        this.showFiltersMenu = !this.showFiltersMenu
      },
      checkValid() {
      /*  if (!this.minDuration) {
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
        } */
      },
      startPollingResults() {
        this.polling = setInterval(() => {
          console.log('polling results')
          this.$store.dispatch('results/fetchResults')          
        }, 3000)
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
    }
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