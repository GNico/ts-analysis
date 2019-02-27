<template>

<div>

  <b-field label="Intervalo agregacion">
    <b-input type="text" v-model="analysisOptions.interval" placeholder="ej: 30m" />
  </b-field>

  <b-field label="Configuracion">
    <b-input type="textarea" v-model="analysisOptions.config" placeholder="ej: {parametro1: p1, otroparametro: op}"></b-input>
  </b-field>


  <b-field class="has-text-right">
    <a class="button is-primary" @click="analize">
      Analizar
    </a>
  </b-field>



</div>




</template>


<script>


export default {
  data () {
    return {
      seriesOptions: {
        name: '',
        client: '',
        contexts: '',
        tags: '',
        start: '',
        end: '',
      },
      analysisOptions: {
        interval: '30m',
        config: ''
      },
      displayOptions: {
        threshold: 0,
        color: '#fff',
        chartType: 'line'
      }
    }
  },
  computed: {
    seriesNames() {
      return this.$store.getters['series/getSeriesNames']
    },
  },
  methods: {
    analize() {
      this.$store.dispatch('series/analizeSeries', this.analysisOptions)
    }
  }

}



</script>

<style>

/*.left-col {
  border-right: 2px solid #282f2f;
}

.series-data {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
}

.series-data__item {
  display: flex;
  align-items: flex-start;
}  

.series-data__item > .label {
  margin-right: 0.5rem;
}  */
</style>