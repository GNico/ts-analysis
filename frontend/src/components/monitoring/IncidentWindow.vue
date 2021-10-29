<template>
<div class="full-page-container">
  <VueDraggableResizable :w="1100" :h="500" :z="999" 
    :handles="['br']"
    @dragging="onDrag" 
    @resizing="onResize" 
    @resizestop="forceRerender"
    :drag-handle="'.drag'"
    :parent="true" >
    <div class="card" :style="{height: '100%'}">
      <header class="card-header drag">
        <p class="card-header-title">
          {{incident.monitor}} → {{incident.analysis.name}}
        </p>
        <button class="transparent-button"  @click="$emit('close')">
          <b-icon icon="close" type="is-primary"></b-icon>
        </button>
      </header>
      <div class="card-content">
        <div class="columns is-paddingless">
          <div class="column is-7">
            <BaseChart 
              :key="chartKey"
              :seriesData="chartData" 
              :bands="chartIncident"
              :style="chartDimensions"
              :extremes="extremes ? extremes : {min: undefined, max:undefined}"/>
          </div>
          <div class="column">
            <div class="is-flex is-flex-direction-column is-justify-content-space-between" :style="{'height': contentHeight + 'px'}">
              <TagCountTable 
                :settings="tableSettings" 
                :compareTo="compareMode"
                @compareChange="compareMode = $event"
                :maxHeight="tableHeight"/>

              <div class="is-flex is-justify-content-space-between">
                <div class="button is-small"> Open</div>
                <div>
                  <div class="button is-small is-primary"> << </div>
                  <div class="button is-small is-primary"> Next >></div>
                </div>
              </div> 

            </div>
          </div>
        </div>
      </div>
    </div>
  </VueDraggableResizable>
</div>
</template>


<script>
import VueDraggableResizable from 'vue-draggable-resizable'
import BaseChart from '@/components/BaseChart'
import { multiseriesTooltipFormatter } from '@/utils/tooltipFormatter'
import TagCountTable from '@/components/analysis/TagCountTable'

export default {
  components: { VueDraggableResizable, BaseChart, TagCountTable },
  props: {
    incident: {
      type: Object,
      default: () => {return {}}    
    }
  },
  data() {
    return {
      chartKey: 0,
      width: 1100,
      height: 500,
      x: 0,
      y: 0,      
      tooltipFormatter: multiseriesTooltipFormatter,
      compareMode: '',
    }
  },
  computed: {
    anomaly() {
      return { from: this.incident.start, to: this.incident.end}
    },
    tableSettings() {
      return {
        client: this.incident.client, 
        data_options: this.incident.analysis.data_options,
        anomalyStart: this.incident.start,
        anomalyEnd: this.incident.end       
      }
    },
    chartData() {
      var cdata = []
      var seriesIds = Object.keys(this.incident.series)
        seriesIds.forEach(seriesId => {
          cdata.push({
            name: 'Input ' + seriesId,
            type: 'line',
            color: '#e7ec98',
            data: this.incident.series[seriesId],
            zIndex: 2,
            fillOpacity: 1,
            enableMouseTracking: true,
            states: {
              hover: {
                lineWidthPlus: 0
              }
            },
          })
        })
      return cdata
    },
    chartIncident() {
      return [{ 
        id: 'p',
        from: Date.parse(this.incident.start),
        to: Date.parse(this.incident.end),
      }]
    },
    contentHeight() {
      return this.height - 100
    },
    tableHeight() {
      return this.contentHeight - 50
    },
    chartDimensions() {
      let w = this.width
      return {
        height: `${this.contentHeight}px`,
        width: `calc((${w}px - 3.75rem)* 0.58)`,
      }
    },
    extremes() {
      var min = Date.parse(this.incident.start)
      var max = Date.parse(this.incident.end)
      return { min: min - 302400000 , max: max + 302400000 }
    }
  },
  methods: {
    onResize: function (x, y, width, height) {
      this.x = x
      this.y = y
      this.width = width
      this.height = height
    },
    onDrag: function (x, y) {
      this.x = x
      this.y = y
    },
    forceRerender() {
      this.chartKey += 1;
    },
  },
  created() {
  }
}

</script>

<style>
.full-page-container {
  position: absolute;
  top: 0;
  left: 0;
  height: 100vh;
  width:  100vw;
}
</style>