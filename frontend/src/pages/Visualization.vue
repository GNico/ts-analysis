<template>
<div>
  <CardSeries 
    :isActive="isOpenSeriesEdit" 
    :id="currentSeriesId"
    @close="isOpenSeriesEdit = false" />
    
  <section class="section p-4">
    <ChartToolbar 
      class="mb-3" 
      :zoomEnabled="zoomEnabled"
      @zoomToggle="toggleZoom"
      @refresh="forceRerender"
      @export="exportSeriesData"/>

    <div class="is-relative is-gapless is-multiline">   
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
              {{item.name ? item.name : 'Series'}}
            </p>
            <b-dropdown-item v-if="item.yAxis > 0" aria-role="listitem" @click="moveUp(item.id)">
              <span><b-icon icon="arrow-up-thick" size="is-small"/> Move up</span>
            </b-dropdown-item>
            <b-dropdown-item v-if="item.yAxis < sortedSeries.length-1" aria-role="listitem" @click="moveDown(item.id)">
              <span><b-icon icon="arrow-down-thick" size="is-small"/> Move down</span>
            </b-dropdown-item>
          </b-dropdown>
          <p v-else>
            {{item.name ? item.name : 'Series'}}
          </p>       
        </LegendSeriesTag>
      </div>
      <Chart 
        :key="componentKey"
        class="is-fullheight"
        :settings="chartSettings"
        :series="series"
        :panels="panels"
        :isLoading="isFetchingData"
        :numAxes="numPanels"
        :range="range"
        :zoomEnabled="zoomEnabled"
        :tagsCount="tagsCount"
        @tagsCountRequest="getTagsCount"
        />
    </div>
  </section>  
</div>
</template>


<script>
import Chart from '../components/visualize/Chart.vue';
import ChartToolbar from '../components/visualize/ChartToolbar.vue';
import LegendSeriesTag from '../components/visualize/LegendSeriesTag.vue';
import CardSeries from '../components/visualize/CardSeries.vue';

import api from "../api/repository";
import { nanoid } from 'nanoid'

export default {
  components: { Chart, ChartToolbar, LegendSeriesTag, CardSeries },
  data () {
    return {
      //backgroundColor: '#073642',
      isOpenSeriesEdit: false,      
      currentSeriesId: '',
      componentKey: 0,
      zoomEnabled: true,
      tagsCount: {}
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
    },
    panels() {
      let panels = []
      this.$store.state.visualize.panels.forEach(panelSeriesIds => {
        panels.push({id: nanoid(), seriesIds: panelSeriesIds})
      })
      return panels
    },
    range() {
      return this.$store.state.visualize.allSeriesRange
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
    toggleZoom() {
      this.zoomEnabled = !this.zoomEnabled
    },
    getTagsCount(request) {
      this.$set(this.tagsCount, request.panelId, [])
      request.seriesIds.forEach(seriesId => {
        let series = this.$store.getters['visualize/getSeriesById'](seriesId)
        api.getTagsCount({
          name: series.client, 
          tags: series.tags,
          contexts: series.contexts,
          start: new Date(request.extremes.min).toISOString(),
          end: new Date(request.extremes.max).toISOString(),
        })
        .then(response => {   
          this.tagsCount[request.panelId].push({
            name: series.name, 
            total: response.data.total, 
            tags: response.data.tags_count
          })
        }) 
      }) 
    },
    forceRerender() {
      this.componentKey += 1;
    },
    exportSeriesData() {
      if (!this.series || !this.series.length>0) return
      let dataStr = JSON.stringify(this.series);
      let dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
      let exportFileDefaultName = 'data.json';
      let linkElement = document.createElement('a');
      linkElement.setAttribute('href', dataUri);
      linkElement.setAttribute('download', exportFileDefaultName);
      linkElement.click();
    }
  },
  watch: {
    numPanels() {
      this.forceRerender()
    }
  },
  created() {
    window.addEventListener('keydown', (e) => {
      if (e.key == 'Control') {
        this.toggleZoom()
      }
    });
  },
}

</script>


<style scoped>
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
</style>