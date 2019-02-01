<template>

<div class="columns is-fullheight ">
  <div class="column is-2 is-sidebar-menu is-hidden-mobile">
      <b-tabs class="side-menu" position="is-centered" type="is-toggle" expanded>
        <b-tab-item label="Series">
            <div class="tab-item-content ">
                <SettingsSeries/>
            </div>
        </b-tab-item>
        <b-tab-item label="Analisis">
            <div class="tab-item-content">
                <SettingsAnalysis/>
            </div>
        </b-tab-item>
      </b-tabs>
  </div>

  <section class="column main-content">
    <div class="box">
      <DateRangeSelect :value="range" @input="changeRange"/>
    </div>
    <div class="chart-container">
      <ChartWrapper/>
    </div>

  </section>
</div>   

</template>


<script>

import ChartWrapper from '../components/ChartWrapper.vue';
import SettingsSeries from '../components/SettingsSeries.vue';
import SettingsAnalysis from '../components/SettingsAnalysis.vue';
import DateRangeSelect from '../components/DateRangeSelect.vue';

export default {
    components: { ChartWrapper, SettingsSeries, SettingsAnalysis, DateRangeSelect },

    data () {
        return {
            selectedRange: { 
                start: null,
                end: null, 
            },
        }
    },
    computed: {
        range() {
            return this.$store.state.series.range
        },
        anomalies() {
            return this.$store.state.series.anomalies
        }
    },
    methods: {
        changeRange(event) {
            this.$store.dispatch('updateRange', event)
        },
    },
}

</script>

