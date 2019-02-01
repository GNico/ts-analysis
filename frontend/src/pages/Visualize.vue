<template>

<div class="columns is-fullheight ">
  <div class="column is-2 is-sidebar-menu is-hidden-mobile">
      <b-tabs class="side-menu" position="is-centered" type="is-toggle" expanded>
        <b-tab-item label="Series">
            <div class="tab-item-content ">
                <SettingsSeries/>
            </div>
        </b-tab-item>
        <b-tab-item label="Analisis">
            <div class="tab-item-content">
                <SettingsAnalysis/>
            </div>
        </b-tab-item>
      </b-tabs>
  </div>

  <section class="column main-content">
    <div class="chart-section">
        <DateRangeSelect :value="range" @input="changeRange"/>
        <ChartWrapper/>
        <BarSeries/>
        <AnomaliesList/>
    </div>  

  </section>
</div>   

</template>



<script>
    
import ChartWrapper from '../components/ChartWrapper.vue';
import SettingsSeries from '../components/SettingsSeries.vue';
import SettingsAnalysis from '../components/SettingsAnalysis.vue';
import DateRangeSelect from '../components/DateRangeSelect.vue';
import BarSeries from '../components/BarSeries.vue';
import AnomaliesList from '../components/AnomaliesList.vue';


export default {

    components: { ChartWrapper, SettingsSeries, SettingsAnalysis, DateRangeSelect, BarSeries, AnomaliesList },

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
            this.$store.dispatch('updateRange', event)
        },
    },
}




</script>


<style lang="sass">  

$section-pad: 5.625rem

.is-sidebar-menu
  overflow: auto

.side-menu
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