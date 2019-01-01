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
                />
              </div>
          </div>


  <div class="tile is-vertical ">
    <div class="tile is-parent">
        <div class="tile is-child notification">
         

          <div class="level">
            <div class="level-left">  
            </div>
            <div class="level-right">
                <div class="level-item">
                    <label class="label">Desde</label>
                </div>
                <div class="level-item">
                    <b-datepicker v-model="selectedRange.start"
                        :first-day-of-week="1"
                        placeholder="Click para seleccionar...">

                        <button class="button is-primary"
                            @click="selectedRange.start = new Date()">
                            <b-icon icon="calendar-today"></b-icon>
                            <span>Today</span>
                        </button>

                        <button class="button is-danger"
                            @click="selectedRange.start = null">
                            <b-icon icon="close"></b-icon>
                            <span>Clear</span>
                        </button>
                    </b-datepicker>
                </div>
                <div class="level-item">
                    <label class="label">Hasta</label>
                </div>
                <div class="level-item">
                    <b-datepicker v-model="selectedRange.end"
                        :first-day-of-week="1"
                        placeholder="Click para seleccionar...">

                        <button class="button is-primary"
                            @click="selectedRange.end = new Date()">
                            <b-icon icon="calendar-today"></b-icon>
                            <span>Today</span>
                        </button>

                        <button class="button is-danger"
                            @click="selectedRange.end = null">
                            <b-icon icon="close"></b-icon>
                            <span>Clear</span>
                        </button>
                    </b-datepicker>
                </div>
                <div class="level-item">
                    <button class="button is-success" @click="updateSeriesData">
                        Actualizar
                    </button>                   
                </div>
            </div>
        </div>


        </div>
    </div>

      <div class="tile">
        <div class="tile is-parent">
          <div class="tile is-child">
            <MainChart :chartData="seriesData" :color="chartColor" :chartType="chartType"></MainChart>
          </div>
        </div>
      </div>
  </div>



    <!-- <div class="tile is-parent">
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
        />
      </div>
    </div> -->


</div>  

</template>



<script>
    
import MainChart from '../components/MainChart.vue';
import SettingsSeries from '../components/SettingsSeries.vue';
import SearchSelect from '../components/SearchSelect.vue';

import { mapState } from 'vuex';


export default {

    components: { MainChart, SettingsSeries, SearchSelect },

    data () {
        return {
            selectedRange: { 
                start: null,
                end: null 
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
        }
    },
    watch: {
        'selectedRange.start': function (newValue) {
            this.$store.commit('set_start_date', newValue)
        },
        'selectedRange.end': function (newValue) {
            this.$store.commit('set_end_date', newValue)
        },
    }
}




</script>