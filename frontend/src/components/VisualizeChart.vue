<template>
<div>
  <ChartSeries class="chart-section" :seriesData="seriesData" :isLoading="loading" :anomalies="chartAnomalies"/> 
  <DateRangeSelect class="chart-section" :range="range" :activeButton="seriesOptions.activeRangeButton" @input="changeSeriesOptions($event); updateData()"/>

</div>


</template>


<script>
import ChartSeries from './ChartSeries.vue';
import DateRangeSelect from '../components/DateRangeSelect.vue';

    
export default {
    components: { DateRangeSelect, ChartSeries },
    data() {
      return {
        
      }
    },
    computed: {
      seriesName() {
        return this.$store.state.analysis.activeSeries
      },
      seriesOptions() {
        return this.$store.getters['analysis/getSeriesOptions'](this.seriesName)
      },
      seriesData() {
        return this.$store.getters['analysis/getDisplaySeriesData']
      },
      range() {
        return { start: this.seriesOptions.start, end: this.seriesOptions.end }
      },
      loading() {
        return this.$store.state.analysis.loading
      },
  /*    chartData() {
        if (!this.seriesData) {
          return []
        } else if (this.seriesOptions.showBaseline && this.baseline) {
          return [ this.seriesData, this.baseline ]
        } else {
          return [ this.seriesData ]
        }
      }, */      
    },
    methods: {
      changeSeriesOptions(options) {
        this.$store.dispatch('analysis/changeSeriesOptions', { name: this.seriesName, options: options})
      },
      updateData() {
        this.$store.dispatch('analysis/fetchSeriesData', this.seriesName)
      },      
    },    
}

</script>


<style>

.chart-section {
  margin-bottom: 0.5rem;
}

</style>