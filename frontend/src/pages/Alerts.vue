<template>

<section class='section'>
  <div class="columns is-fullheight">

    <div class="column is-3 side-menu is-hidden-mobile">        
      <b-tabs type="is-toggle" expanded size="is-small">
        <b-tab-item label="Analysis" icon-pack="fas" icon="chart-line">
          <AnalysisSettings/>
        </b-tab-item>
        <b-tab-item label="Results" icon-pack="fas" icon="file-alt">
          <AnomaliesList/> 
        </b-tab-item>
      </b-tabs>
    </div>

    <div class="column main-content">
      <AnalysisChart 
        :seriesData="seriesData"
        :baseline="baseline"
        :anomalies="anomalies"
        :loading="loading"
        />
      <hr>        
    </div>

  </div>  
</section> 

</template>


<script>
import AnalysisChart from '../components/AnalysisChart.vue';
import AnalysisSettings from '../components/AnalysisSettings.vue';
import AnomaliesList from '../components/AnomaliesList.vue';


export default {
    components: { AnalysisChart, AnalysisSettings, AnomaliesList },
    computed: {
      seriesData() {
        return this.$store.state.analysis.results.series
      },
      baseline() {
        return this.$store.state.analysis.results.baseline
      },
      anomalies() {
        return this.$store.state.analysis.results.anomalies
      },
      loading() {
        return this.$store.state.analysis.loading
      },
    },
    methods: {
    },
}

</script>



<style>

.section {
  padding: 1rem;
}

.is-fullheight {
  height: calc(100vh - 9rem);
  min-height: calc(100vh - 9rem);
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
</style>