<template>
<div>
  <ChartSeries class="chart-section" :seriesData="chartData" :isLoading="loading" :anomalies="chartAnomalies"/> 
  
  <div class="chart-footer chart-section">
    <div class="chart-footer-section">
      <div class="chart-footer__field">
        <label class="checkbox label">
          <input type="checkbox" :checked="showBaseline" v-model="showBaseline">
          Show baseline
        </label>
      </div>
      <div class="chart-footer__field">
   <!--     <label class="label"> Score threshold</label>
        <input class="slider is-marginless" type="range" step="1" min="0" max="100" 
              v-model="scoreValue" 
              @change="changeSeriesOptions({scoreThreshold: $event.target.value})">
        <label class="tag is-info label"> {{ scoreValue }}</label>   -->

      </div>
    </div>



  </div>
</div>


</template>


<script>
import ChartSeries from './ChartSeries.vue';

    
export default {
    components: { ChartSeries },
    data() {
      return {
        scoreValue: 0,
        showBaseline: true,
      }
    },
    computed: {
      seriesData() {
        return this.$store.state.analysis.results.series
      },
      baseline() {
        return this.showBaseline ? this.$store.state.analysis.results.baseline : []
      },
      anomalies() {
        return this.$store.state.analysis.results.anomalies
      },
      loading() {
        return this.$store.state.analysis.loading
      },
      chartData() {
      /*  if (!this.seriesData) {
          return []
        } else if (this.showBaseline && this.baseline) {
          return [ this.seriesData, this.baseline ]
        } else { */
          return  this.seriesData 
        
      },
      chartAnomalies() {
        var vm = this
        var anoms = []
        for (var item of this.anomalies) {
          anoms.push({id: item.id,
                     from: item.from,
                     to: item.to,
                     color: 'blue',
                     events: {
                      click: function(e) {
                        vm.setActiveAnomaly(this.options.id)
                      } 
                     }
                    })
        }
        return anoms
      }
    },
    methods: {
      setActiveAnomaly(id) {
        this.$store.dispatch('analysis/setActiveAnomaly', id)
    }
  },
}
</script>


<style>
.chart-section {
  margin-bottom: 0.25rem;
}

.chart-section > * {
  margin: 0 0.5rem 0.5rem 0
}

.chart-footer {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  margin-right: -1rem;
}

.chart-footer-section {
  display: flex;
  align-items: baseline; 
}

.chart-footer__field {
  display: flex;
  align-items: baseline;
  margin-right: 1rem;
}

.chart-footer__field > .label {
  margin-left: 0.25rem;
  margin-right: 0.25rem;
}  

.color-box {
  visibility: hidden;
}
</style>