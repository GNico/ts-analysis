<template>
<div>
  <BarSeries :activeSeries="activeSeries" @change="setActiveSeries"/>

  <section class='page-container'>
    <div class="columns is-fullheight">

      <div class="column is-2 side-menu is-hidden-mobile">        
        <b-tabs type="is-toggle" expanded size="is-small">
          <b-tab-item label="Analysis" icon-pack="fas" icon="chart-line">
            <SettingsAnalysis/>
          </b-tab-item>
          <b-tab-item label="Details" icon-pack="fas" icon="file-alt">
            <span> nothing here </span>
          </b-tab-item>
        </b-tabs>
      </div>

      <div class="column main-content">
        <AnalysisChart/>
        <hr>
        <AnomaliesList/>         
      </div>

    </div>  
  </section> 
</div>
</template>



<script>
import BarSeries from '../components/BarSeries.vue';
import AnalysisChart from '../components/AnalysisChart.vue';
import SettingsAnalysis from '../components/SettingsAnalysis.vue';
import AnomaliesList from '../components/AnomaliesList.vue';


export default {
    components: { BarSeries, AnalysisChart, SettingsAnalysis, AnomaliesList },
    computed: {
      activeSeries() {
        return this.$store.state.analysis.activeSeries
      }
    },
    methods: {
      setActiveSeries(event) {
        this.$store.dispatch("analysis/setActiveSeries", event)
      }
    },
}
</script>


<style>

.page-container {
  padding: 1.25rem;
}

.is-fullheight {
  height: calc(100vh - 9rem);
  min-height: calc(100vh - 9rem);
}
  
.side-menu {
  overflow-y: overlay;
}

.main-content {
  display: flex;
  flex-direction: column;
  overflow-y: overlay;
  overflow-x: hidden;
}
</style>