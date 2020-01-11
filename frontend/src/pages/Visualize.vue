<template>

<div class="container">
  <div class="section is-flex">
    
     <div class="card tagcontainer">
      <TreeView :items="tags" :displayItems="displayElements" v-model="selectedItems" />
    </div>
  </div>
</div>
<!-- <div>
  <div class="columns is-fullheight ">
     <div class="column is-2 side-menu is-hidden-mobile">
        <SettingsVisualize/>   
    </div> 

    <section class="column main-content">
      <div class="chart-section">

          <BarSeries section="visualize"/>
          <DateRangeSelect :value="range" @input="changeRange"/>

      </div>  

    </section>
  </div>   
</div> -->
</template>



<script>
import api from '../api/repository'


import SettingsSeries from '../components/SettingsSeries.vue';
import SettingsVisualize from '../components/SettingsVisualize.vue';
import DateRangeSelect from '../components/DateRangeSelect.vue';
import BarSeries from '../components/BarSeries.vue';

import TreeView from '../components/TreeView.vue';


export default {
  components: { SettingsSeries, SettingsVisualize, DateRangeSelect, BarSeries, TreeView },
  data () {
    return {
      selectedRange: { 
        start: null,
        end: null, 
      },
      tags: { name: 'All tags', id: "root", children: [] },
      displayElements: {},
      selectedItems: [],
      flatData: [ 'root' ],
    }
  },
  methods: {
    changeRange(event) {
      this.$store.dispatch('visualize/updateRange', event)
    },
    selectAllNodes(event) {
      if (event) {
        this.selectedItems = this.flatData
      } else {
        this.selectedItems = []
      }
    }
  },
  created () {
    api.getTags('movistar')
    .then(response => {       
      this.tags.children = response.data.tree
      this.displayElements = { name: this.tags.name,
                               id: this.tags.id,
                               children: [] }
    })


  },
}




</script>


<style lang="sass">  

$section-pad: 5.625rem

.side-menu
  overflow: auto


.is-fullheight
  height: calc(100vh - 9.625rem) 
  min-height: calc(100vh - 9.625rem) 

.main-content 
  display: flex
  flex-direction: column
  overflow-y: auto
    
.chart-section > *
  margin: 0 0.5rem 0.5rem 0

.tagcontainer
  max-height: 30rem
  max-width: 30rem
  overflow: auto

</style>