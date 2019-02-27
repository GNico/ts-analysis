<template>
<div>
  <BarSeries :activeSeries="activeSeries" @change="setActiveSeries"/>
  <div class="columns is-fullheight ">

    <div class="column is-2 side-menu is-hidden-mobile ">
      <b-tabs type="is-boxed" expanded size="is-small">
        <b-tab-item label="Analysis" icon-pack="fas" icon="chart-line">
          <SettingsAnalysis/>
        </b-tab-item>
        <b-tab-item label="Details" icon-pack="fas" icon="file-alt">

        </b-tab-item>
      </b-tabs>
    </div>

    <div class="column main-content">
      <AnalysisChart/>
<!--       <AnomaliesList/>
 -->    </div>
  </div>   
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
.is-fullheight {
  height: calc(100vh - 9.625rem);
  min-height: calc(100vh - 9.625rem);
}
  
.side-menu {
  overflow: auto;
}

.main-content {
  display: flex;
  flex-direction: column;
  overflow-y: auto;
}
</style>