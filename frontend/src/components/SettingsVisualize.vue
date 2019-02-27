<template>
<div>

  <div class="field">
    <label class="label"> Nombre </label>
    <b-field>
      <b-select placeholder="" expanded :value="displayOptions.name" @input="setSavedOptions"> 
        <option v-for="item in seriesNames"> {{ item }}</option>
      </b-select>     
    </b-field>
  </div>
  
  <div class="field">
      <label class="label"> Tipo de grafico </label>
      <div class="select">
        <select v-model="displayOptions.chartType">
            <option>line</option>
            <option>areaspline</option>
            <option>spline</option>
            <option>scatter</option>
            <option>column</option>
            <option>area</option>
        </select>
      </div>
  </div>

  <div class="field">
      <label class="label"> Intervalo display </label>
      <div class="select">
        <select v-model="displayOptions.interval">
            <option value="30m">30 minutos</option>
            <option value="1H">1 hora</option>
            <option value="2H">2 horas</option>
            <option value="6H">6 horas</option>
            <option value="12H">12 horas</option>
            <option value="1d">1 dia</option>
        </select>
      </div>
  </div>

  <div class="field">
      <label class="label"> Color </label>
      <SelectColor v-model="displayOptions.color"/> 
  </div>


  <!-- buttons  -->
  <div v-if="edit" class="box has-text-centered">
    <a class="button is-primary" @click="updateSeries">
        Actualizar
    </a>
  </div>
  <div v-else class="buttons is-centered box">
      <a class="button is-primary" @click="addSeries">
        Agregar
      </a>
<!--       <a class="button is-danger" @click="editMode">
        Cancelar
      </a> -->
  </div>
</div>

</template>



<script>

import SelectColor from './SelectColor.vue';
import SelectChartType from './SelectChartType.vue';
import SearchSelect from './SearchSelect.vue';

export default {
    components: { SelectColor, SelectChartType, SearchSelect },
    data () {
        return {
            displayOptions: {
                name: '',
                color: '#6fcd98',
                chartType: 'line',
                interval: '1H'
            },
        }
    },
    computed: {
        seriesNames() {
            return this.$store.getters['series/getSeriesNames']
        },
        displaySeriesNames() {
            return this.$store.getters['visualize/getSeriesNames']
        },
        edit() {
          return this.displaySeriesNames.includes(this.displayOptions.name)
        }
    },
    methods: {
        setSavedOptions (value) {
            let obj = this.$store.getters['visualize/getSeriesOptions'](value) 
            this.displayOptions.name = value
            this.displayOptions.color = obj.color
            this.displayOptions.chartType = obj.chartType
            this.displayOptions.interval = obj.interval
        },
        addSeries() {
            this.$store.dispatch('visualize/addSeries', this.displayOptions)
        },
        updateSeries() {
            this.$store.dispatch('visualize/updateSeries', this.displayOptions)
        },
        clearFields() {
            this.displayOptions.name = ''
            this.displayOptions.color = '#6fcd98'      
            this.displayOptions.chartType = 'line'
            this.displayOptions.interval = '1H'

        },
    },
    watch: {
        seriesNames() {
            /*if (!this.seriesNames.includes(this.displayOptions.name) && this.edit) {
                this.clearFields()
            } */
        }
    }
}

</script>