<template>


<div>
  <section class="section">
    <VisualizeToolBar class="char-bar"/>

    <div class="chart-container columns is-gapless is-multiline">   
      <div class="column is-1 char-sec" :style="{ 'background-color': backgroundColor }">
        <div class="legends">
          <LegendSeriesTag 
            v-for="item in series"
            :color="item.color"
            :id="item.id"
            @delete="removeSeries"
            @show="toggleSeriesVisibility"
            @settings="openSeriesSettings">
            {{item.name}}
          </LegendSeriesTag>
        </div>
      </div>
      <div class="column is-offset-1 is-11 char-sec " >
        <VisualizeChart 
          class="is-fullheight"
          :backgroundColor="backgroundColor"
          :series="series"
          :isLoading="isFetchingData"
          :numAxes="numPanels"/>
      </div>
    </div>
  </section>

  <ModalCard 
    :isActive="isOpenSeriesEdit" 
    @close="isOpenSeriesEdit=false">
    <template v-slot="{closeHandler}">
      <VisualizeCardSeriesEdit  @close="closeHandler"/>
    </template>  
  </ModalCard>

</div>
</template>

<script>

import VisualizeChart from '../components/VisualizeChart.vue';
import VisualizeToolBar from '../components/VisualizeToolBar.vue';
import LegendSeriesTag from '../components/LegendSeriesTag.vue';

import ModalCard from '../components/ModalCard.vue';
import VisualizeCardSeriesEdit from '../components/VisualizeCardSeriesEdit.vue';



export default {
  components: { VisualizeChart, VisualizeToolBar, LegendSeriesTag, ModalCard, VisualizeCardSeriesEdit },
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
    numPanels() {
      return this.$store.getters['visualize/numPanels']
    },
    currentSeries() {
      return this.$store.getters['visualize/getSeriesById'](this.currentSeriesId)
    },
    isFetchingData() {
      return this.$store.state.visualize.loading > 0
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
    }
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
  z-index: 99999;
}

.section {
  padding: 1rem;
}
</style>