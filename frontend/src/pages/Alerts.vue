<template>
<div>
  <ExpChart :chartData="chartData" :popularTags="popularTags" @selection="getInfo"/>
</div>
</template>


<script>
import api from "../api/repository";

import ExpChart from "../components/ExpChart";

export default {
  components: { ExpChart },
  data () {
    return {
      chartData: [],
      popularTags: [],
    }
  },
  computed: {
    
  },
  methods: {
    getInfo(extremes) {
      api.getTagsCount({
        name: "treetest",
        start: new Date(extremes.min).toISOString(),
        end: new Date(extremes.max).toISOString(),
        size: 5
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
        name: "treetest",
      })
      .then(response => {       
        this.chartData = response.data
      })
      .catch(error => { 
        console.log('error')
        console.log(error)
      })
  }
}

</script>