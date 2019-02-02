<template>


<div class="columns">
  <div class="column is-6 left-col">

  <h3 class="title is-4">Serie</h3>
  <div class="series-data">
    <div class="series-data__item">
      <label class="label"> Nombre </label>
      <b-input value=""></b-input>
    </div>

    <div class="series-data__item">
      <label class="label"> Cliente </label>
      <b-input value=""></b-input>
    </div>

    <div class="series-data__item">
      <label class="label"> Contexto </label>
      <b-input value=""></b-input>
    </div>

    <div class="series-data__item">
      <label class="label"> Tags </label>
      <b-input value=""></b-input>
    </div>

    <div class="series-data__item">
      <label class="label"> Desde </label>
      <b-input value=""></b-input>
    </div>

    <div class="series-data__item">
      <label class="label"> Hasta </label>
      <b-input value=""></b-input>
    </div>


  </div>

  </div>
  
  <div class="column is-6">

  <h3 class="title is-4">Analisis</h3>

  <div class="series-data">

    <div class="series-data__item">
      <label class="label"> Intervalo agregacion </label>
      <b-input type="text" v-model="analysisOptions.interval" placeholder="ej: 30m" />
    </div>

    <div class="series-data__item">
      <label class="label"> Desde </label>
      <b-input type="textarea" v-model="analysisOptions.config" placeholder="ej: {parametro1: p1, otroparametro: op}"></b-input>
    </div>

    <div>
      <a class="button is-primary" @click="analize">
        Analizar
      </a>
    </div>
  </div>

  </div>

</div>


</template>


<script>


export default {
  data () {
    return {
      analysisOptions: {
        name: '',
        interval: '30m',
        config: ''
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

.left-col {
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
}  
</style>