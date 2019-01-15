<template>
<!--Grid -->
<div class="tile is-ancestor">

  <div class="tile is-parent is-2">
      <div class="tile is-child box">


            <b-tabs position="is-centered" type="is-toggle" expanded>
                <b-tab-item label="Series">
                    <div class="tab-item-content">
                        <SettingsSeries/>
                    </div>

                </b-tab-item>
                <b-tab-item label="Analisis">
                    <div class="tab-item-content">
                        <SettingsAnalysis @analize="startAnalysis"/>
                    </div>
                </b-tab-item>

                <b-tab-item label="Comparar">

                </b-tab-item>

            </b-tabs>
        
      </div>
  </div>


  <div class="tile is-vertical">


    <div class="tile is-parent ">
        <div class="tile is-child box ">

          <DateRangeSelect :value="range" @input="changeRange"/>

        </div>
    </div>


    <div class="tile is-parent ">
        <div class="tile is-child box ">

          <BarSeries/>

        </div>
    </div>

    <div class="tile">
      <div class="tile is-parent">
        <div class="tile is-child">

          <ChartWrapper/>

        </div>
      </div>
    </div>
  </div>


</div>  

</template>



<script>
    
import ChartWrapper from '../components/ChartWrapper.vue';
import SettingsSeries from '../components/SettingsSeries.vue';
import SettingsAnalysis from '../components/SettingsAnalysis.vue';
import DateRangeSelect from '../components/DateRangeSelect.vue';
import BarSeries from '../components/BarSeries.vue';


export default {

    components: { ChartWrapper, SettingsSeries, SettingsAnalysis, DateRangeSelect, BarSeries },

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
        startAnalysis() {
            this.$store.dispatch('fetchAnomalies');
        },
        changeRange(event) {
            this.$store.commit('set_range', event)
        },
    },
}




</script>


<style>
.tab-item-content {
    margin-top: 1rem;
}

</style>