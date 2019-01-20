<template>
<div>

  <div class="field">
    <label class="label"> Serie </label>
    <b-field>
      <b-select placeholder="" expanded v-model="analysisOptions.name"> 
        <option v-for="item in seriesNames"> {{ item }}</option>
      </b-select>     
    </b-field>
  </div>

  <b-field label="Intervalo bucket">
    <input class="input" type="text" v-model="analysisOptions.interval" placeholder="ej: 30m">
  </b-field>

  <b-field label="Config (temporario)">
    <textarea class="textarea" v-model="analysisOptions.config" placeholder="ej: {parametro1: p1, otroparametro: op}"></textarea>
  </b-field>

  <div class="box has-text-centered">
    <a class="button is-primary" @click="analize">
      Analizar
    </a>
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
      return this.$store.getters.getSeriesNames
    },
  },
  methods: {
    analize() {
      this.$store.dispatch('analizeSeries', this.analysisOptions)
    }
  }

}



</script>