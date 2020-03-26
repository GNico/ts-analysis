<template>
<div>
  <DateRangeSelect class="chart-section" :range="range" :activeButton="seriesOptions.activeRangeButton" @input="changeSeriesOptions($event); updateData()"/>
  <ChartSeries class="chart-section" :seriesData="chartData" :isLoading="loading" :anomalies="chartAnomalies"/> 
  <div class="chart-footer chart-section">

    <div class="chart-footer-section">
      <div class="chart-footer__field">
        <label class="checkbox label">
          <input type="checkbox" :checked="seriesOptions.showBaseline" :value="seriesOptions.showBaseline" @change="changeSeriesOptions({showBaseline: !seriesOptions.showBaseline})">
          Show baseline
        </label>
      </div>
      <div class="chart-footer__field">
        <label class="label"> Score threshold</label>
        <input class="slider is-marginless" type="range" step="1" min="0" max="100" 
              v-model="scoreValue" 
              @change="changeSeriesOptions({scoreThreshold: $event.target.value})">
        <label class="tag is-info label"> {{ scoreValue }}</label>  

      </div>
    </div>

    <div class="chart-footer-section">
      <div class="chart-footer__field">
        <label class="label"> Intervalo </label>
        <div class="select is-small">
          <select :value="seriesOptions.interval" @change="changeSeriesOptions({interval: $event.target.value}); updateData()">
            <option value="30m">30 minutos</option>
            <option value="1H">1 hora</option>
            <option value="2H">2 horas</option>
            <option value="6H">6 horas</option>
            <option value="12H">12 horas</option>
            <option value="1d">1 dia</option>
          </select>
        </div>
      </div>

      <div class="chart-footer__field">
        <label class="label"> Tipo de grafico </label>
        <div class="select is-small">
          <select :value="seriesOptions.chartType" @change="changeSeriesOptions({chartType: $event.target.value})">
            <option>line</option>
            <option>areaspline</option>
            <option>spline</option>
            <option>scatter</option>
            <option>column</option>
            <option>area</option>
          </select>
        </div>
      </div>
       <div class="chart-footer__field">
        <label class="label"> Color </label>
        <label class="input is-small" :style="{ backgroundColor: seriesOptions.color}" >
          <input class="input is-small color-box" type="color" :value="seriesOptions.color" @change="changeSeriesOptions({color: $event.target.value })"> 
        </label>
      </div>
    </div>



  </div>
</div>


</template>


<script>
import ChartSeries from './ChartSeries.vue';
import DateRangeSelect from '../components/DateRangeSelect.vue';

    
export default {
    components: { DateRangeSelect, ChartSeries },
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
      seriesData() {
        return this.$store.getters['analysis/getDisplaySeriesData']
      },
      baseline() {
        return this.$store.getters['analysis/getDisplayBaseline']
      },
      anomalies() {
        return this.$store.getters['analysis/getDisplayAnomalies']
      },
      range() {
        return { start: this.seriesOptions.start, end: this.seriesOptions.end }
      },
      loading() {
        return this.$store.state.analysis.loading
      },
      chartData() {
        if (!this.seriesData) {
          return []
        } else if (this.seriesOptions.showBaseline && this.baseline) {
          return [ this.seriesData, this.baseline ]
        } else {
          return [ this.seriesData ]
        }
      },
      chartAnomalies() {
        var vm = this
        var anoms = []
        for (var item of this.anomalies) {
          anoms.push({id: item.id,
                     from: item.from,
                     to: item.to,
                     color: item.color,
                     events: {
                      click: function(e) {
                        vm.setActiveAnomaly(this.options.id)
                      } 
                     }
                    })
        }
        return anoms
      }
    },
    methods: {
      changeSeriesOptions(options) {
        this.$store.dispatch('analysis/changeSeriesOptions', { name: this.seriesName, options: options})
      },
      updateData() {
        this.$store.dispatch('analysis/fetchSeriesData', this.seriesName)
      },
      setActiveAnomaly(id) {
        this.$store.dispatch('analysis/setActiveAnomaly', id)
      }
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


<style>
.chart-section {
  margin-bottom: 0.25rem;
}

.chart-section > * {
  margin: 0 0.5rem 0.5rem 0
}

.chart-footer {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  margin-right: -1rem;
}

.chart-footer-section {
  display: flex;
  align-items: baseline; 
}

.chart-footer__field {
  display: flex;
  align-items: baseline;
  margin-right: 1rem;
}

.chart-footer__field > .label {
  margin-left: 0.25rem;
  margin-right: 0.25rem;
}  

.color-box {
  visibility: hidden;
}
</style>