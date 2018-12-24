<template>
<!--Grid -->
<div class="tile is-ancestor">
  <div class="tile is-vertical is-9">
    <div class="tile is-parent">
        <div class="tile is-child notification">
          <div class="level">
            <div class="level-left">
                <div class="level-item">
                    <label class="label">Cliente</label>
                </div>
                <div class="level-item">
                        <b-autocomplete
                            v-model="name"
                            placeholder="Seleccionar cliente"
                            open-on-focus
                            :data="filteredDataArray"
                            field="name"
                            @select="option => selected = option">
                            <template slot="empty">No hay resultados para {{name}}</template>
                        </b-autocomplete>
                 </div>
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
            <MainChart :color="chartColor" :chartType="chartType"></MainChart>
          </div>
        </div>
      </div>
  </div>



    <div class="tile is-parent">
      <div class="tile is-child notification">
        <VisualizePanel @color-changed="changeSeriesColor" @type-changed="changeChartType"/>
      </div>
    </div>

    


</div>  

</template>



<script>
    
import MainChart from '../components/MainChart.vue';
import VisualizePanel from '../components/VisualizePanel.vue';
import { mapState } from 'vuex';


export default {

    components: { MainChart, VisualizePanel },

    data () {
        return {
            selectedRange: { 
                start: null,
                end: null 
            },
            selected: null,
            name: '',
            chartColor: "#6fcd98",
            chartType: "line"

        }
    },
    computed: {
        clients() {
            return this.$store.state.series.clients
        },
        range() {
            return this.$store.state.series.range
        },
        filteredDataArray() {
            return  this.clients.filter(
                (item) => {return item.name.toLowerCase().match(this.name.toLowerCase())} )
        }
    },
    methods: {
        updateSeriesData() {
            this.$store.dispatch('fetchData');
        },
        changeSeriesColor(event) {
            this.chartColor = event.selected
        },
        changeChartType(event) {
            this.chartType = event.selected
        }
    },
    watch: {
        'selectedRange.start': function (newValue) {
            this.$store.commit('set_start_date', newValue)
        },
        'selectedRange.end': function (newValue) {
            this.$store.commit('set_end_date', newValue)
        },
        name(newValue) {
            this.$store.commit('set_client_name', newValue)
            this.$store.dispatch('fetchContexts')
            this.$store.dispatch('fetchTags')
        }
    }
}




</script>