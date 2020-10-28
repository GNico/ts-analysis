<template>

<div class="fill-height-or-more">
  <BaseChart v-for="seriesData in chartSeriesData" 
    :key="seriesData.id" 
    :seriesData="seriesData" 
    :loading="isLoading"
    :extremes="extremes"
    @changedExtremes="syncExtremes"
    />
</div>
</template>


<script>
import BaseChart from "./BaseChart";

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
    }
  },
  computed: {
    chartSeriesData() {
      let allSeriesData = []
      this.panels.forEach(panel => {
        var seriesData = []
        panel.forEach(seriesid => {
          var s1 = this.series.find(elem => elem.id === seriesid)
          seriesData.push({
            name: s1.name,
            data: s1.data,
            id: s1.id,
            color: s1.color,
            visible: s1.visible,
            lineWidth: this.lineWidth,
            states: {
               hover: {
                  lineWidth: this.lineWidth
               },          
            },
          })
          if (this.range.start) { //invisible series to force extremes
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
          if (this.range.end) { //invisible series to force extremes
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
        allSeriesData.push(seriesData)
      })
      return allSeriesData 
    },
  },
  methods: {  
    syncExtremes(event) {
      this.extremes = event
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