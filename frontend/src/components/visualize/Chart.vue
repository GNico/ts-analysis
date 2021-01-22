<template>

<div class="fill-height-or-more">
  <BaseChart v-for="panel in chartSeriesData" 
    :key="panel.id"
    :seriesData="panel.data" 
    :settings="settings"
    :labelContent="transform(panel.id)"
    :zoomEnabled="zoomEnabled"
    :loading="isLoading"
    :extremes="extremes"
    @changedExtremes="syncExtremes"
    @crosshairMove="syncCrosshairs"
    :crosshair="crosshair"
    :syncCrosshairEnabled="true"
    @selection="getTagsCount(panel.id, $event)"

  />
</div>
</template>


<script>
import BaseChart from "../BaseChart";

export default {
  components: { BaseChart },
  props: {   
    series: {
      type: Array,
      default: () => []
    },
    panels: {
      type: Array,
      default: () => []
    },
    numAxes: {
      type: Number,
      default: 1    
    },
    range: {
      type: Object,
      default: () => {return {
        start: null,
        end: null
      }}
    },
    tagsCount: {
      type: Object,
      default: () => {}
    },
    zoomEnabled: {
      type: Boolean,
      default: true
    },
    isLoading: {
      type: Boolean,
      default: false
    },
    settings: {
      type: Object,
      default: () => {}
    },
  },
  data () {
    return {
      updateArgs: [true, true, false],
      extremes: {},
      crosshair: {},
    }
  },
  computed: {
    chartSeriesData() {
      let allSeriesData = []
      this.panels.forEach(panel => {      
        var seriesData = []
        panel.seriesIds.forEach(seriesid => {
          var s1 = this.series.find(elem => elem.id === seriesid)
          seriesData.push({
            id: s1.id,
            name: s1.name,
            data: s1.data,
            type: s1.type,
            color: s1.color,
            visible: s1.visible,
            lineWidth: this.settings.lineWidth,
            states: {
              hover: {
                lineWidth: this.settings.lineWidth
              },          
            },
          })
          if (this.range.start) { //invisible series to force out of bound extremes
            seriesData.push({
              data: [{
                x: this.range.start,
                y: 0
              }],
              color: 'rgba(0,0,0,0)',
              enableMouseTracking: false,
              showInLegend: false
            })
          }
          if (this.range.end) { //invisible series to force out of bound extremes
            seriesData.push({
              data: [{
                x: this.range.end,
                y: 0
              }],
              color: 'rgba(0,0,0,0)',
              enableMouseTracking: false,
              showInLegend: false
            })
          }
        })
        allSeriesData.push({id: panel.id , data: seriesData})
      })
      return allSeriesData 
    },
  },
  methods: {  
    transform(panelId) {
      var text = ''
      if (this.tagsCount[panelId]) {
        this.tagsCount[panelId].forEach((series, index) => {
          text += '<table class="table is-narrow is-bordered is-fullwidth has-text-grey has-background-black">'
          text += '<thead><tr><th colspan="2" ><strong class="has-text-grey-light">' + series.name + '</strong> </th> </thead>'
          series.tags.forEach(elem => {
            text += '<tr><td class="has-text-right has-text-grey-light">' + ((elem.count * 100) / series.total).toFixed(1) + '%</td>' 
            text += '<td> ' +  elem.tag + '</td>'
          })
        })
        text += '</table>'
      }
      return text
    },
    syncExtremes(event) {
      this.extremes = event
    },  
    syncCrosshairs(event) {
      this.crosshair = event
    },
    getTagsCount(panelId, extremes) {
      let seriesIds = []
      let panel = this.chartSeriesData.find(elem => elem.id == panelId)
      panel.data.forEach(series => {
        if (series.id)  //filter invisible series
          seriesIds.push(series.id)
      })
      this.$emit('tagsCountRequest', {panelId: panelId, seriesIds: seriesIds, extremes: extremes }) 
    },
  }, 
  watch: {
    range: {
      //deep: true,
      handler(newval) {
        this.extremes = { }
      }
    }
  } 
}

</script>



<style scoped>
.fill-height-or-more {
  display: flex;
  flex-direction: column;
}

.fill-height-or-more > * {
  flex: 1;
}
</style>