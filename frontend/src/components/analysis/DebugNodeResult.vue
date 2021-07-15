<template>
<div class="columns" :style="{height: height + 'px'}">
  <div class="column chart-column is-flex is-flex-direction-column">
    <div class="is-flex is-justify-content-space-between mb-2 is-align-items-center ">
      <!--header left section-->
      <b-dropdown trap-focus>
        <template #trigger>            
          <a class="is-flex is-align-items-center has-text-white">
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
                  <div v-for="entry in Object.entries(node.paramsData)" :label="entry[0]" class="ml-4">
                    <span> {{entry[0]}}: {{entry[1]}} </span>
                  </div>
                </section>                            
            </div>
        </b-dropdown-item>
      </b-dropdown>
      
      <!--header right section-->
      <div class="is-flex is-align-items-center">              
        <b-dropdown  class="header-item" aria-role="list" v-model="axisInterval">
            <template #trigger>
              <a class="is-flex is-align-items-center has-text-grey">
                <span><strong>Axis interval: {{axisInterval}}</strong></span>
                <b-icon icon="menu-down"></b-icon>
              </a>
            </template>
            <b-dropdown-item aria-role="listitem" value="auto">auto</b-dropdown-item>
            <b-dropdown-item aria-role="listitem" value="month">month</b-dropdown-item>
            <b-dropdown-item aria-role="listitem" value="week">week</b-dropdown-item>
            <b-dropdown-item aria-role="listitem" value="day">day</b-dropdown-item>
            <b-dropdown-item aria-role="listitem" value="hour">hour</b-dropdown-item>
        </b-dropdown>   
        <b-checkbox v-model="showMinMax">
          <strong class="has-text-grey">Show min and max values</strong>
        </b-checkbox>   
      </div>      
    </div>

    <!--chart section -->
    <Chart     
      class="is-flex-grow-1"
      :seriesData="series"
      :anomalies="anomalies"
      :loading="loading"
      :activeAnomaly="activeAnomalyId"
      :range="extremes"
      :syncCrosshairEnabled="true"
      :showMinMax="showMinMax"
      :axisInterval="axisInterval"
      @changeActive="activeAnomalyId = $event"
      @updateRange="updateRange"
    />
  </div>

  <div class="column is-4 is-flex is-flex-direction-column" :style="{height: height + 'px'}">     
      <div class="mb-2 is-flex" >
        <div class="mr-4 is-clickable" @click="activeTab = 0"> 
          <strong :class="activeTab == 0 ? 'has-text-white' : ''"> Node details </strong> 
        </div>
        <div class="mr-4 is-clickable" @click="activeTab = 1" v-if="anomalies && anomalies.length">
          <strong :class="activeTab == 1 ? 'has-text-white' : ''"> Anomalies</strong>
        </div>
        <div class="mr-4 is-clickable" @click="activeTab = 2" v-if="debug_info">
          <strong :class="activeTab == 2 ? 'has-text-white' : ''"> Debug info</strong>
        </div>
      </div>


      <div v-if="node.paramsData && activeTab == 0" class="is-flex-grow-1">
        <div class="mt-2 has-text-grey-light"> Description: </div>
        <div class="ml-4 mb-2"> {{node.desc}} </div>
        <div class="has-text-grey-light"> Parameters: </div>
        <div v-for="entry in Object.entries(node.paramsData)" :label="entry[0]" class="ml-4">
          <span> {{entry[0]}}: {{entry[1]}} </span>
        </div>
      </div>

      <AnomaliesTable   
        v-else-if="activeTab == 1"
        class="is-flex-grow-1"
        id="anom-table"
        :anomalies="anomalies"
        :activeAnomaly="activeAnomalyId"
        @changeActive="activeAnomalyId = $event"
      /> 

      <div v-else-if="activeTab == 2 && debug_info">
        <div v-for="(value, key) in debug_info">
          <span class="has-text-grey-light">{{key}}:</span> {{value}}
        </div>
      </div>
  </div>
</div> 
  

</template>

<script>
import AnomaliesTable from './AnomaliesTable'
import Chart from './Chart'

export default {
  components: { AnomaliesTable, Chart },
  props: {
    result: {
      type: Object,
      default: () => {return {}} 
    },
    height: {
      type: Number,
      default: 450,
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
      showMinMax: true,
      axisInterval: 'auto',

      activeTab: 0
    }
  },
  computed: {
    series() {
      return this.result.series
    },
    anomalies() {
      return this.result.anomalies
    },
    debug_info() {
      return this.result.debug_info
    }
  },
  methods: {
    updateRange(event) {
      this.$emit('updateRange', event)
    },
  }
}
</script>


<style scoped>
.chart-column {
  border-right: 2px solid rgba(255,255,255,0.1);
}

.param-separator {
  background-color: rgba(255,255,255,0.1);
  height: 1px;
  margin: 1rem 0 1rem 0;
}

.header-item {
  border-right: 1px solid rgba(255,255,255,0.2);
  padding-right: 0.75rem;
  margin-right: 0.75rem;
}

</style>