<template>

<div>

  <div class="columns">
    <div class="column page-section">
      <SettingsAnalysis/>
    </div>
  </div>


  <div class="columns ">
    <div class="column is-2  is-hidden-mobile  ">
        <AnalysisDisplayOptions/>
    </div>

    <div class="column">
      <div class="">
          <ChartWrapper/>
          <AnomaliesList/>
      </div>  
    </div>
  </div>   

</div>
</template>



<script>
    
import ChartWrapper from '../components/ChartWrapper.vue';
import SettingsSeries from '../components/SettingsSeries.vue';
import SettingsAnalysis from '../components/SettingsAnalysis.vue';
import AnalysisDisplayOptions from '../components/AnalysisDisplayOptions.vue';
import AnomaliesList from '../components/AnomaliesList.vue';


export default {

    components: { ChartWrapper, SettingsSeries, SettingsAnalysis, AnalysisDisplayOptions, AnomaliesList },

    data () {
        return {
            selectedRange: { 
                start: null,
                end: null, 
            },
        }
    },
    computed: {
        range() {
            return this.$store.state.series.range
        },
        anomalies() {
            return this.$store.state.series.anomalies
        }
    },
    methods: {
        changeRange(event) {
            this.$store.dispatch('series/updateRange', event)
        },
    },
}




</script>


<style lang="sass">  

$section-pad: 5.625rem


.page-section
  background-color: #343c3d
  border-radius: 8px 


.is-fullheight
  height: calc(100vh - 9.625rem) 
  min-height: calc(100vh - 9.625rem) 

.main-content 
  display: flex
  flex-direction: column
  overflow-y: auto
    
.chart-section > *
  margin: 0 0.5rem 0.5rem 0


</style>