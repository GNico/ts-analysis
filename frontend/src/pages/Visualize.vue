<template>
<!--Grid -->
<div class="tile is-ancestor">

  <div class="tile is-parent is-2">
      <div class="tile is-child box">


            <b-tabs position="is-centered" type="is-toggle" expanded>
                <b-tab-item label="Series">
                    <div class="tab-item-content">
                        <SettingsSeries 
                            :clients="clientsSelectOptions"
                            :contexts="contexts"
                            :tags="tags"
                            @context-selected="changeContext" 
                            @client-selected="changeClient"
                            @tag-selected="changeTag" 
                            @color-selected="changeSeriesColor" 
                            @type-selected="changeChartType"
                            @update="updateSeriesData"/>
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

          <ChartSeries 
              :chartData="seriesData" 
              :color="chartColor" 
              :chartType="chartType"
              :anomalies="anomalies" />

        </div>
      </div>
    </div>
  </div>


</div>  

</template>



<script>
    
import ChartSeries from '../components/ChartSeries.vue';
import SettingsSeries from '../components/SettingsSeries.vue';
import SettingsAnalysis from '../components/SettingsAnalysis.vue';
import DateRangeSelect from '../components/DateRangeSelect.vue';
import BarSeries from '../components/BarSeries.vue';

import { mapState } from 'vuex';


export default {

    components: { ChartSeries, SettingsSeries, SettingsAnalysis, DateRangeSelect, BarSeries },

    data () {
        return {
            selectedRange: { 
                start: null,
                end: null, 
            },
            clientName: '',
            chartColor: "#6fcd98",
            chartType: "line",
        }
    },
    computed: {
        clients() {
            return this.$store.state.series.clients
        },
        clientsSelectOptions() {
            return this.clients.map(item => item.name);
        },
        contexts() {
            return this.$store.state.series.contexts
        },
        tags() {
            return this.$store.state.series.tags
        },
        range() {
            return this.$store.state.series.range
        },
        seriesData() {
            return this.$store.state.series.data
        },
        anomalies() {
            return this.$store.state.series.anomalies
        }
    },
    methods: {
        updateSeriesData() {
            this.$store.dispatch('fetchData');
        },
        startAnalysis() {
            this.$store.dispatch('fetchAnomalies');
        },
        changeSeriesColor(event) {
            this.chartColor = event
        },
        changeChartType(event) {
            this.chartType = event.selected
        },
        changeClient(event) {
            this.$store.dispatch('changeCurrentClient', event.selected)
        },
        changeContext(event) {
            this.$store.commit('set_current_context', event.selected)
        },
        changeTag(event) {
            this.$store.commit('set_current_tag', event.selected)
        },
        changeRange(event) {
            this.$store.commit('set_range', event)
            this.updateSeriesData()
        },
    },
}




</script>


<style>
.tab-item-content {
    margin-top: 1rem;
}

</style>