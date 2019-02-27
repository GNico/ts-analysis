<template>

<div>
  <div class="columns is-fullheight ">
     <div class="column is-2 side-menu is-hidden-mobile">
        <SettingsVisualize/>   
        <!-- <b-tabs class="side-menu" position="is-centered" type="is-toggle" expanded>
          <b-tab-item label="Series">
            <div class="tab-item-content ">
              <SettingsVisualize/>                  
            </div>
          </b-tab-item>
          <b-tab-item label="Analisis">
            <div class="tab-item-content">
                
            </div>
          </b-tab-item>
        </b-tabs> -->
    </div> 

    <section class="column main-content">
      <div class="chart-section">

          <BarSeries section="visualize"/>
          <DateRangeSelect :value="range" @input="changeRange"/>
          <!-- <ChartWrapper/> -->

      </div>  

    </section>
  </div>   
</div>
</template>



<script>
    
import SettingsSeries from '../components/SettingsSeries.vue';
import SettingsVisualize from '../components/SettingsVisualize.vue';
import DateRangeSelect from '../components/DateRangeSelect.vue';
import BarSeries from '../components/BarSeries.vue';


export default {
  components: { SettingsSeries, SettingsVisualize, DateRangeSelect, BarSeries },
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
      return this.$store.state.visualize.range
    },
  },
  methods: {
    changeRange(event) {
      this.$store.dispatch('visualize/updateRange', event)
    },
  },
}




</script>


<style lang="sass">  

$section-pad: 5.625rem

.side-menu
  overflow: auto


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