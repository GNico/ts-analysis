<template>

<div class="fill-height-or-more">
  <BaseChart v-for="panel in chartSeriesData" 
    :key="panel.id"
    :seriesData="panel.data" 
    :labelContent="transform(panel.id)"
    :zoomEnabled="zoomEnabled"
    :loading="isLoading"
    :extremes="extremes"
    @changedExtremes="syncExtremes"
    @crosshairMove="syncCrosshairs"
    :crosshair="crosshair"
    :syncCrosshairEnabled="false"
    @selection="getTagsCount($event, panel.id)"

  />
</div>
</template>


<script>
import BaseChart from "./BaseChart";

//labelContent[panel.id]
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
    backgroundColor: {
      type: String,
      default: ''
    },
    lineWidth: {
      type: Number,
      default: 2
    },
    marginLeft: {
      type: Number,
      default: 100
    },
    marginTop: {
      type: Number,
      default: 0
    },
    marginBottom: {
      type: Number,
      default: 0
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
            lineWidth: this.lineWidth,
            states: {
              hover: {
                lineWidth: this.lineWidth
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
    labelContent() {
      return "asd"
     /* let content = {}
      this.tagsCount.forEach(panel => {
        var text = ''
        panel.series.forEach(series => {
          text += '<strong>' + series.name + '</strong> <br>'
          for (var elem of series.tags) {
            text += elem.tag + ': ' + elem.count + ' <br>'
          }     
        })
        content[panel.id] = text
      })
      return content */
    }
  },
  methods: {  
    transform(panelId) {
      var text = ''
      if (this.tagsCount[panelId]) {
        this.tagsCount[panelId].forEach(series => {
          text += '<strong>' + series.name + '</strong> <br>'
          for (var elem of series.tags) {
            text += elem.tag + ': ' + elem.count + ' <br>'
          }   
        })
      }
      return text
    },
    syncExtremes(event) {
      this.extremes = event
    },  
    syncCrosshairs(event) {
      this.crosshair = event
    },
    getTagsCount(extremes, panelId) {
      console.log(panelId)
      let seriesIds = []
      let panel = this.chartSeriesData.find(elem => elem.id = panelId)
      panel.data.forEach(series => {
        if (series.id)  //filter invisible series
          seriesIds.push(series.id)
      })
      this.$emit('tagsCountRequest', {panelId: panelId, seriesIds: seriesIds, extremes: extremes })
    },

  },  
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