<template>

<div class="container">
  <div class="section">
    <div class="card tagcontainer">
      <TreeView :items="tags" :displayItems="displayElements" v-model="selectedItems" @togglechildren="toggleChildren"/>
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
      tags: {},
      displayElements: {},
      selectedItems: [],
      treeData: {
        name: 'All Tags',
        id: 'root',
        children: [
          { id: 1, 
            name: 'first' },
          { id: 2,
            name: 'second' },
          { 
            name: 'third child',
            children: [
              { 
                name: 'grandchild',
                children: [
                  { id: 5,
                    name: 'someone' },
                  { id: 6,
                    name: 'noone' }
                ]
              },
              { id: 7,
                name: 'hello' },
              { id: 8,
                name: 'wat' },
              { name: 'anotherone',
                children: [
                  { id: 10,
                    name: 'ups' },
                  { id: 11,
                    name: 'kek' }
                ]
              }
            ]
          }
        ]
      }
    }
  },
  computed: {
    subtag() {
      let newarray = this.tags.children.slice(9,10)
      let newobj = { name: "All tags", id: "root", children: newarray  } 
      return newobj
    },
    chunks() {
      let tagNumbers = []
      this.tags.children.forEach(child => {
        let number = 0
        let searchTree = items => {
          if (!! items.children && items.children.length > 0) {
            number = number + items.children.length
            items.children.forEach(child => searchTree(child))
          } 
        }
        searchTree(child)
        tagNumbers.push(number)
      })
      return tagNumbers
      //.sort(function(a, b) {return a - b;})
    },    
  },
  methods: {
    changeRange(event) {
      this.$store.dispatch('visualize/updateRange', event)
    },
    toggleChildren(event) {
      if (event.shouldDisplay) {
        this.showChildren(event.id)
      } else {
        this.hideChildren(event.id)
      }
    },
    showChildren(id) {
      let name_list = id.split("_")
      let displaydic = this.displayElements
      let tagsdic = this.tags
      if (name_list[0] != "root") {
        name_list.forEach(name => {
          tagsdic = tagsdic.children.find(x => x.name === name)
          displaydic = displaydic.children.find(x => x.name === name)
        })
      }
      //add  the next layer of children if not already there
      if (displaydic['children'].length == 0) {
        tagsdic['children'].forEach(child => {
          let newchild = {id: child.id, name: child.name}
          if (child.hasOwnProperty('children')) {
            newchild['children'] = []
          }
          displaydic['children'].push(newchild)
        })
      }
    },
    hideChildren(id) {
      let name_list = id.split("_")
      let displaydic = this.displayElements
      if (name_list[0] != "root") {
        name_list.forEach(name => {
          displaydic = displaydic.children.find(x => x.name === name)
        })
      }
      if (displaydic['children'].length > 0) {
        displaydic['children'] = []
      }
    }
  },
  created () {
    api.getTags('movistar')
    .then(response => {       
      this.tags = response.data
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