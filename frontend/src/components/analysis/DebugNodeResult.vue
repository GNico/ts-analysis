<template>
<div  class="columns" :style="expanded ? {height: height + 'px'} : ''">
  <a v-if="!expanded" class="is-flex is-align-items-center m-3 has-text-white" @click="expanded = !expanded">
    <b-icon icon="menu-right"></b-icon>
    <span><strong>{{node.display}} {{node.id ? '(' + node.id + ')' : ''}}</strong></span>
  </a>

  <template v-else>
  <div class="column chart-column is-flex is-flex-direction-column">
    <div class="is-flex is-justify-content-space-between mb-2 is-align-items-center">
      <!--header left section-->
      <a class="is-flex is-align-items-center has-text-white" @click="expanded = !expanded">
        <b-icon icon="menu-down"></b-icon>
        <span><strong>{{node.display}} {{node.id ? '(' + node.id + ')' : ''}}</strong></span>
      </a>
      
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
      :anomalies="filteredAnomalies"
      :loading="loading"
      :activeAnomaly="activeAnomalyId"
      :range="extremes"
      :forcedMaxRange="chartsRange"
      :syncCrosshairEnabled="true"
      :showMinMax="showMinMax"
      :axisInterval="axisInterval"
      @changeActive="activeAnomalyId = $event"
      @updateRange="updateRange"
    />
  </div>

  <div class="column is-4 is-flex is-flex-direction-column" :style="{height: height + 'px'}">     
    <!--tabs headers-->  
    <div class="mb-2 is-flex">
      <div class="mr-4 is-clickable" @click="selectedTab = 1" v-if="!isEmpty(node.paramsData)"> 
        <strong :class="activeTab == 1 ? 'has-text-white' : ''"> Node details </strong> 
      </div>
      <div class="mr-4 is-clickable" @click="selectedTab = 2" v-if="anomalies && anomalies.length">
        <strong :class="activeTab == 2 ? 'has-text-white' : ''"> Anomalies </strong>
      </div>
      <div class="mr-4 is-clickable" @click="selectedTab = 3" v-if="debug_info">
        <strong :class="activeTab == 3 ? 'has-text-white' : ''"> Debug info </strong>
      </div>
    </div>

    <!--tabs content-->  
    <div v-if="!isEmpty(node.paramsData) && activeTab == 1" class="is-flex-grow-1 scrollable">
      <div class="mt-2 has-text-grey-light"> Name: </div>
      <div class="ml-4 mb-2"> {{node.display}} </div>
      <div class="mt-2 has-text-grey-light"> Description: </div>
      <div class="ml-4 mb-2"> {{node.desc}} </div>
      <div class="has-text-grey-light"> Parameters: </div>
      <div v-for="entry in Object.entries(node.paramsData)" :label="entry[0]" class="ml-4">
        <span> {{entry[0]}}: {{entry[1]}} </span>
      </div>
    </div>

    <AnomaliesTable v-else-if="activeTab == 2 && !isEmpty(anomalies)"
      :height="tableHeight"
      :anomalies="filteredAnomalies"
      :activeAnomaly="activeAnomalyId"
      :debug="true"
      @changeActive="activeAnomalyId = $event"/> 

    <div v-else-if="activeTab == 3 && !isEmpty(debug_info)" class="is-flex-grow-1 scrollable" >
      <div v-for="(value, key) in debug_info">
        <span class="has-text-grey-light">{{key}}:</span> 
        <span class="param-text" v-if="!key.includes('chart')"> {{value}} </span>
        <DebugChart 
          v-else
          :style="{height:'200px'}"
          :title="key"
          :data="value"/>
      </div>      
    </div>
  </div>
  </template>
</div> 
</template>

<script>
import AnomaliesTable from '@/components/analysis/AnomaliesTable'
import Chart from '@/components/analysis/Chart'
import DebugChart from '@/components/analysis/DebugChart'
import isEmpty from "lodash/isEmpty";

export default {
  components: { AnomaliesTable, Chart, DebugChart },
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
    chartsRange: {
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
      selectedTab: null,
      expanded: true,
    }
  },
  computed: {
    series() {
      return this.result.series
    },
    anomalies() {
      return this.result.anomalies
    },
    filteredAnomalies() {
      return this.anomalies.filter(elem =>           
        (!this.extremes.start || parseInt(elem.from) > this.extremes.start)
        && (!this.extremes.end || parseInt(elem.from) < this.extremes.end))
    }, 
    debug_info() {
      return this.result.debug_info
    },
    activeTab() {
      var active = 1 
      if (!this.selectedTab) {
        if (!this.isEmpty(this.anomalies)) {
          active = 2 
        } else if (!this.isEmpty(this.debug_info)) {
          active = 3
        }
      } else {
        active = this.selectedTab
      }
      return active
    },
    tableHeight() {
      return `calc(${this.height}px - 3.5rem)`
    }   
  },
  methods: {
    updateRange(event) {
      this.$emit('updateRange', event)
    },
    isEmpty(elem) {
      return isEmpty(elem)
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

.scrollable {
  overflow-y: auto;
}

.param-text {
  white-space: pre;
  font-family: monospace;
  font-size: 0.65vw;  /*magic number to make text adjust to container*/
}
</style>