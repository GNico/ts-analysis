<template>

<div v-else class="columns" :style="{height: height + 50 + 'px'}">
  <div class="column main-content" :style="{height: height + 'px'}">
    <div class="section-header ">
      <b-dropdown
        trap-focus>
        <template #trigger>            
          <a class="node-title has-text-white">
            <span><strong>{{node.display}}</strong></span>
            <b-icon v-if="node.paramsData" icon="menu-down"></b-icon>
          </a>
        </template>

        <b-dropdown-item
          v-if="node.paramsData"
          aria-role="menu-item"
          :focusable="false"
          custom
          paddingless>
            <div class="modal-card" style="max-width:300px;">
                <section class="modal-card-body">
                  <div> {{node.desc}} </div>
                  <hr class="param-separator">
                  <div> Parameters: </div>
                  <div v-for="entry in Object.entries(node.paramsData)" :label="entry[0]" class="param-list">
                    <span> {{entry[0]}}: {{entry[1]}} </span>
                  </div>
                </section>                            
            </div>
        </b-dropdown-item>
      </b-dropdown>
    </div>

    <Chart     
      class="thechart"
      :seriesData="series"
      :baseline="baseline"
      :anomalies="anomalies"
      :loading="loading"
      :activeAnomaly="activeAnomalyId"
      :range="extremes"
      @changeActive="activeAnomalyId = $event"
      @updateRange="updateRange" />
  </div>

  <div class="column is-4" :style="{height: height + 'px'}">     
    <template v-if="anomalies.length">
      <div class="section-header has-text-white">
        <div> <strong class="has-text-grey-light"> Anomalies</strong></div>
     <!--   <AnomaliesFilters v-bind="filters" @update="updateOptions"/>  -->
      </div>

      <AnomaliesTable   
        id="anom-table"
        :anomalies="anomalies"
        :activeAnomaly="activeAnomalyId"
        @changeActive="activeAnomalyId = $event"
        /> 
    </template>
  </div>
</div> 
  

</template>

<script>
import AnomaliesTable from './AnomaliesTable'
//import AnomaliesFilters from './AnomaliesFilters'
import Chart from './Chart'

export default {
  components: { AnomaliesTable, Chart },
  props: {
    series: {
      type: Array,
      default: () => []
    },
    anomalies: {
      type: Array,
      default: () => []
    },
    baseline: {
      type: Array,
      default: () => []
    },
    height: {
      type: Number,
      default: 400,
    },
    extremes: {
      type: Object,
      default: () => {return {}}
    },
    node: {
      type: Object,
      default: () => {return {}}
    }
  },
  data () {
    return {
      loading: false,
      activeAnomalyId: '',
  /*    filters: {
        showBaseline: true,
        showSeries: true,
        showTrend: false,
        scoreThreshold: 0,
        minDuration: '',
        minDurationTime: 0,        
      }    */
    }
  },
  computed: {
  /*  filteredAnomalies() {
      return this.anomalies.filter(elem =>         
        (!this.extremes.start || parseInt(elem.from) > this.extremes.start)
        && (!this.extremes.end || parseInt(elem.from) < this.extremes.end))
    },  */
/*    filteredActiveAnomaly() {
      let filteredAnom = this.filteredAnomalies.find(elem => elem.id === this.activeAnomalyId)
      return filteredAnom ? filteredAnom.id : ''
    }, */
  },
  methods: {
    updateRange(event) {
      this.$emit('updateRange', event)
    },
  /*  updateOptions(event) {
      this.filters = { ...this.filters, ...event }
    } */
  }
}
</script>



<style scoped>
/*.main-content {
  display: flex;
  flex-direction: column;
  overflow-y: overlay;
  overflow-x: hidden;
} */
.node-title {
  display: flex;
  align-items: center;
}

.param-separator {
  background-color: rgba(255,255,255,0.1);
  height: 1px;
  margin: 1rem 0 1rem 0;
}

.param-list {
  margin-left: 1rem;
}

.thechart {
  height: inherit;
}

.section-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
  align-items: center;
  height: 30px;
}

</style>