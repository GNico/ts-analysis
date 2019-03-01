<template>

<div>

  <b-field label="Intervalo agregacion">
    <b-input type="text" :value="seriesOptions.analysisInterval" placeholder="ej: 30m" @input="changeSeriesOptions({analysisInterval: $event})" />
  </b-field>

  <b-field label="Configuracion">
    <b-input type="textarea" :value="seriesOptions.config" placeholder="ej: {parametro1: p1, otroparametro: op}" @input="changeSeriesOptions({config: $event})"></b-input>
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
  computed: {
    seriesName() {
      return this.$store.state.analysis.activeSeries
    },
    seriesOptions() {
      return this.$store.getters['analysis/getSeriesOptions'](this.seriesName)
    },
  },
  methods: {
    analize() {
      this.$store.dispatch('analysis/analizeSeries', this.seriesName)
    },
    changeSeriesOptions(options) {
      this.$store.dispatch('analysis/changeSeriesOptions', { name: this.seriesName, options: options})
    },
  }
}
</script>