<template>

<div>

  <div class='page-container'>
    <section class="page-section">
      <div class="level">

        <div class="level-left">
          <template v-if="popo">
            <div class="level-item">
              <div class="button is-primary">New Visualization</div>
            </div>
            <div class="level-item">
              or
            </div>
            <div class="level-item">
              <b-dropdown aria-role="list">
                  <button class="button" slot="trigger" slot-scope="{ active }">
                      <span>Select Visualization</span>
                      <b-icon :icon="active ? 'caret-up' : 'caret-down'"></b-icon>
                  </button>
                  <b-dropdown-item aria-role="listitem">  <b-tooltip label="description" type="is-dark" position="is-right">Action</b-tooltip></b-dropdown-item>
                  <b-dropdown-item aria-role="listitem">Another action</b-dropdown-item>
                  <b-dropdown-item aria-role="listitem">Something else</b-dropdown-item>
              </b-dropdown>
            </div>
          </template>
        </div>

        <div class="level-right">
          <SearchSelect 
            :saved="[]"
            :data="[]"
            placeholder="Select client" 
            ref=clientselect
          />
        </div>
        
      </div>
    </section>

    <hr>

    <section class="page-section">
      <div class="title is-3 has-text-link"> Unnamed Visualization {{ test }}
      </div> 
    </section>


    <section>
      <VisualizeBarSeries/>
    </section>

    <section class="columns is-variable is-2">
      <div class="column is-2 ">

        <div class="is-fullheight side-menu">        
          <b-collapse
            class="card"
            animation="slide"
            v-for="(collapse, index) of collapses"
            :key="index"
            :open="false">

            <div
              slot="trigger"
              slot-scope="props"
              class="card-header"
              role="button">    
              <p class="card-header-title">
                  {{ collapse.title }}
              </p>
              <a class="card-header-icon">
                  <b-icon
                      :icon="props.open ? 'caret-up' : 'caret-down'">
                  </b-icon>
              </a>
            </div>
            <div class="card-content">
                <div class="content">
                  <component :is="collapse.component"> </component>
                </div>
            </div>
          </b-collapse>
        </div>
      </div>

      <div class="column">
        <div class="main-content is-fullheight">
          <VisualizeChart/>
        </div>
      </div>

    </section>  
  </div> 
</div>
</template>



<script>
import api from '../api/repository'

import VisualizeChart from '../components/VisualizeChart.vue';
import VisualizeBarSeries from '../components/VisualizeBarSeries.vue';
import VisualizeMenuVisualization from '../components/VisualizeMenuVisualization.vue';
import VisualizeMenuData from '../components/VisualizeMenuData.vue';
import VisualizeMenuChartSettings from '../components/VisualizeMenuChartSettings.vue';
import VisualizeMenuIndicators from '../components/VisualizeMenuIndicators.vue';
import SearchSelect from '../components/SearchSelect.vue';



export default {
  components: { VisualizeChart, VisualizeBarSeries, VisualizeMenuVisualization, VisualizeMenuData,
                VisualizeMenuChartSettings, VisualizeMenuIndicators, SearchSelect },
  data () {
    return {
      isOpen: [],
      popo: true,
      collapses: [
      {
          title: 'Visualization',
          component: 'VisualizeMenuVisualization'
      },
      {
          title: 'Data',
          component: 'VisualizeMenuData'
      },
      {
          title: 'Chart settings',
          component: 'VisualizeMenuChartSettings'
      },
      {
          title: 'Indicators',
          component: 'VisualizeMenuIndicators'
      }
      ],
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
  computed: {
    test() {
      return this.$store.state.visualize.nest.name
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


<style>  

.page-container {
  padding: 1.25rem;
}

.page-section {
  margin-bottom: 1.25rem;
}

.subsection {
  margin-bottom: 0.75rem;
}

.is-fullheight {
  height: calc(100vh - 20rem);
  min-height: calc(100vh - 20rem);
}
  
.side-menu {
  overflow-y: auto;
}

.main-content {
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  overflow-x: hidden;
}


</style>