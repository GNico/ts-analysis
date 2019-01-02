<template>
<!--Grid -->
<div class="tile is-ancestor">
  <div class="tile is-parent is-2">
      <div class="tile is-child notification">

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
  </div>
  <div class="tile is-vertical ">
    <div class="tile is-parent">
        <div class="tile is-child notification">

          <DateRangeSelect :value="range" @input="changeRange"/>

        </div>
    </div>

    <div class="tile">
      <div class="tile is-parent">
        <div class="tile is-child">

          <MainChart 
              :chartData="seriesData" 
              :color="chartColor" 
              :chartType="chartType" />

        </div>
      </div>
    </div>
  </div>


</div>  

</template>



<script>
    
import MainChart from '../components/MainChart.vue';
import SettingsSeries from '../components/SettingsSeries.vue';
import DateRangeSelect from '../components/DateRangeSelect.vue';

import { mapState } from 'vuex';


export default {

    components: { MainChart, SettingsSeries, DateRangeSelect },

    data () {
        return {
            selectedRange: { 
                start: null,
                end: null, 
            },
            clientName: '',
            chartColor: "#6fcd98",
            chartType: "line"

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
    },
    methods: {
        updateSeriesData() {
            this.$store.dispatch('fetchData');
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