<template>

<div v-else class="columns" :style="{height: height + 50 + 'px'}">
  <div class="column main-content" :style="{height: height + 'px'}">
    <div class="section-header ">
      <b-dropdown
        trap-focus>
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
    </div>

    <Chart     
      class="thechart"
      :seriesData="series"
      :baseline="baseline"
      :anomalies="anomalies"
      :loading="loading"
      :activeAnomaly="activeAnomalyId"
      :range="extremes"
      :syncCrosshairEnabled="true"
      @changeActive="activeAnomalyId = $event"
      @updateRange="updateRange"
       />
  </div>

  <div class="column is-4" :style="{height: height + 'px'}">     
    <template v-if="anomalies.length">
      <div class="section-header has-text-white">
        <div> <strong class="has-text-grey-light"> Anomalies</strong></div>
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
    }
  },
  computed: {
  },
  methods: {
    updateRange(event) {
      this.$emit('updateRange', event)
    },
  }
}
</script>


<style scoped>
.param-separator {
  background-color: rgba(255,255,255,0.1);
  height: 1px;
  margin: 1rem 0 1rem 0;
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