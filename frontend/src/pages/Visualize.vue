<template>


<div>
  <section class="section">
    <VisualizeToolBar class="char-bar"/>

    <div class="chart-container columns is-gapless is-multiline">   
        <div class="legends">
          <LegendSeriesTag 
            v-for="item in sortedSeries"
            :key="item.id"
            :color="item.color"
            :id="item.id"
            @delete="removeSeries"
            @show="toggleSeriesVisibility"
            @settings="openSeriesSettings">

            <b-dropdown  v-if="sortedSeries.length > 1" aria-role="list"">
              <p slot="trigger" role="button">
                {{item.name}}
              </p>
              <b-dropdown-item v-if="item.yAxis > 0" aria-role="listitem" @click="moveUp(item.id)">
                <span><b-icon icon="arrow-up-thick" size="is-small"/> Move up</span>
              </b-dropdown-item>
              <b-dropdown-item v-if="item.yAxis < sortedSeries.length-1" aria-role="listitem" @click="moveDown(item.id)">
                <span><b-icon icon="arrow-down-thick" size="is-small"/> Move down</span>
              </b-dropdown-item>
            </b-dropdown>
            <p v-else>
              {{item.name}}
            </p>       
          </LegendSeriesTag>
        </div>
      <div class="column is-offset-1 is-12 char-sec" >
        <VisualizeChart 
          class="is-fullheight"
          :backgroundColor="chartSettings.backgroundColor"
          :lineWidth="chartSettings.lineWidth"
          :marginLeft="chartSettings.marginLeft"
          :marginTop="chartSettings.marginTop"
          :marginBottom="chartSettings.marginBottom"
          :series="series"
          :isLoading="isFetchingData"
          :numAxes="numPanels"/>
      </div>
    </div>
  </section>

  
 
  <VisualizeCardSeries 
    :isActive="isOpenSeriesEdit" 
    :id="currentSeriesId"
    @close="isOpenSeriesEdit = false" />
  

</div>
</template>

<script>

import VisualizeChart from '../components/VisualizeChart.vue';
import VisualizeToolBar from '../components/VisualizeToolBar.vue';
import LegendSeriesTag from '../components/LegendSeriesTag.vue';

import VisualizeCardSeries from '../components/VisualizeCardSeries.vue';



export default {
  components: { VisualizeChart, VisualizeToolBar, LegendSeriesTag, VisualizeCardSeries },
  data () {
    return {
      backgroundColor: '#073642',
      isOpenSeriesEdit: false,
      currentSeriesId: ''
    }
  },
  computed: {
    series() {
      return this.$store.getters['visualize/seriesAsList']
    },
    sortedSeries() {
      function compare(a, b) {
        if (a.yAxis < b.yAxis)
          return -1;
        if (a.yAxis > b.yAxis)
          return 1;
        return 0;
      }
      return this.series.sort(compare);
    },
    numPanels() {
      return this.$store.getters['visualize/numPanels']
    },
    currentSeries() {
      return this.$store.getters['visualize/getSeriesById'](this.currentSeriesId)
    },
    isFetchingData() {
      return this.$store.state.visualize.loading > 0
    },
    chartSettings() {
      return this.$store.state.visualize.settings
    }
  },
  methods: {
    removeSeries(id) {
      this.$store.dispatch("visualize/deleteSeries", id)
    },
    toggleSeriesVisibility(e) {
      let newoptions = { visible: !e.hidden }
      this.$store.dispatch("visualize/updateSeries", { id: e.id, seriesOptions: newoptions })
    },
    openSeriesSettings(id) {
      this.currentSeriesId = id
      this.isOpenSeriesEdit = true
    },
    moveUp(id) {
      this.$store.dispatch("visualize/moveSeriesUp", id)
    },
    moveDown(id) {
      this.$store.dispatch("visualize/moveSeriesDown", id)
    },
  }
}

</script>

<style scoped>

.char-bar {
  margin-bottom: 0.75rem;
}

.chart-container { 
  position: relative;
 }

.char-sec {
  height: inherit;
}

.is-fullheight {
  height: calc(100vh - 8.5rem);
  min-height: calc(100vh - 8.5rem);
}

.legends {
  position: absolute;
  z-index: 999;
}

.section {
  padding: 1rem;
}
</style>