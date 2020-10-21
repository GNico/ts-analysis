<template>
<div>
  <BaseChart :seriesData="chartData" 
            :labelContent="labelContent" 
            :zoomEnabled="zoomEnabled"
            @selection="getInfo"
            @changedExtremes="sync"
            @crosshair="syncCrosshairs"
            :extremes="extremes"
            :syncCrosshair="syncCrosshair"
            :syncCrosshairEnabled="true"/>

  <BaseChart :seriesData="chartData" 
            :labelContent="labelContent" 
            :zoomEnabled="zoomEnabled"
            @selection="getInfo"
            @changedExtremes="sync"
            :extremes="extremes"
            @crosshair="syncCrosshairs"
            :syncCrosshair="syncCrosshair"
            :syncCrosshairEnabled="true"/>

  <BaseChart :seriesData="chartData" 
          :labelContent="labelContent" 
          :zoomEnabled="zoomEnabled"
          @selection="getInfo"
          @changedExtremes="sync"
          :extremes="extremes"
          :syncCrosshair="syncCrosshair"/>         




</div>
</template>


<script>
import api from "../api/repository";

import BaseChart from "../components/BaseChart";

export default {
  components: { BaseChart },
  data () {
    return {
      chartData: [],
      popularTags: [],
      zoomEnabled: true,
      extremes: {},
      syncCrosshair: {},
    }
  },
  computed: {
    labelContent() {
      var text = ''
      for (var elem of this.popularTags) {
        text += elem.tag + ': ' + elem.count + ' <br>'
      }
      return text
    }
  },
  methods: {
    sync(event) {
      this.extremes = event
    },
    syncCrosshairs(event) {
      this.syncCrosshair = event
    },
    getInfo(extremes) {
      api.getTagsCount({
        name: "movistar",
        start: new Date(extremes.min).toISOString(),
        end: new Date(extremes.max).toISOString(),
      })
      .then(response => {       
        this.popularTags = response.data
      })
      .catch(error => { 
        console.log('error')
        console.log(error)
      })
    }
  },
  mounted: function () {
    api.getSeriesData({ 
        name: "movistar",
      })
      .then(response => {       
        this.chartData = response.data
      })
      .catch(error => { 
        console.log('error')
        console.log(error)
      })
  },
  created() {
    window.addEventListener('keydown', (e) => {
      if (e.key == 'Control') {
        this.zoomEnabled = !this.zoomEnabled;
      }
    });
  },
}

</script>