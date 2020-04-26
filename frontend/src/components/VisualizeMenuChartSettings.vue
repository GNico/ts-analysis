<template>
<div>
  <b-field label="Interval">
    <b-select size="is-small" :value="seriesOptions.interval" @change="changeSeriesOptions({interval: $event.target.value}); updateData()">
      <option value="30m">30 minutes</option>
      <option value="1H">1 hour</option>
      <option value="2H">2 hour</option>
      <option value="6H">6 hours</option>
      <option value="12H">12 hours</option>
      <option value="1d">1 day</option>
    </b-select>
  </b-field>

  <b-field label="Chart type">
    <b-select size="is-small" :value="seriesOptions.chartType" @change="changeSeriesOptions({chartType: $event.target.value})">
      <option>line</option>
      <option>areaspline</option>
      <option>spline</option>
      <option>scatter</option>
      <option>column</option>
      <option>area</option>
    </b-select>
  </b-field>

  <b-field label="Series color" class=''>
      <label class="input is-small color-box" :style="{ backgroundColor: seriesOptions.color}" >
        <input class="input is-small color-input" type="color" :value="seriesOptions.color" @change="changeSeriesOptions({color: $event.target.value })"> 
      </label>
  </b-field>
</div>
</template>



<script>
  
export default {
    components: {   },
    data() {
      return {
        scoreValue: 0,
      }
    },
    computed: {
      seriesName() {
        return this.$store.state.analysis.activeSeries
      },
      seriesOptions() {
        return this.$store.getters['analysis/getSeriesOptions'](this.seriesName)
      },
      
    },
    methods: {
      changeSeriesOptions(options) {
        this.$store.dispatch('analysis/changeSeriesOptions', { name: this.seriesName, options: options})
      },
      updateData() {
        this.$store.dispatch('analysis/fetchSeriesData', this.seriesName)
      },
    },
    watch: {
      'seriesOptions.scoreThreshold': {
        handler: function (newval) {
          this.scoreValue = newval
        },
        immediate: true
      }
    }
}

</script>


<style scoped>

.color-input {
  visibility: hidden;
}

.color-box {
  max-width: 30%;
}

</style>