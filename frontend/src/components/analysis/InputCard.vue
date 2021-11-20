<template>
<div>
  <b-collapse
    class="card"
    animation="slide"
    :open="isOpen"
    @open="sharedState.openNode = inputNumber.toString()"
    @close="sharedState.openNode = null">
    <template #trigger="props">
      <div class="card-header" @mouseover="showDelete = true" @mouseleave="showDelete = false" >
        <span class="card-header-title long-text-with-ellipsis">
          <span v-if="showDelete" class="tag is-danger is-family-monospace p-1 mr-1" @click="deleteInput"> &nbsp;X&nbsp; </span>
          <span v-else class="tag is-info  is-family-monospace p-1 mr-1"> &nbsp;{{inputNumber}}&nbsp; </span>
          <span class="has-text-grey-light">  &nbsp; Input </span>
        </span>
        <a class="card-header-icon">
          <b-icon :icon="props.open ? 'menu-up' : 'menu-down'"/>
        </a>
      </div>     
    </template> 

    <div class="card-content">
      <div class="content">
        <b-field horizontal label="Client">        
          <SearchSelect
            :value="analysis.client"
            @input="updateAnalysis('client', $event, true)"
            :data="allClients"/>
        </b-field>
        <div class="mb-3 filters-box is-flex">
          <div class="label field-label"> Tags </div>
          <TreeSelect 
            class="treebody"
            rootName="All tags"
            filterName="Filter by tags"
            :itemsTree="tagOptions"
            :value="dataOptions.tags"
            :applyFilter="dataOptions.filterTags"
            @input="updateAnalysis('tags', $event, false)"
            @filterCheck="updateAnalysis('filterTags', $event, false)"
          />
        </div>
        <div class="mb-3 filters-box is-flex">
          <div class="label field-label"> Contexts </div>
          <TreeSelect 
            class="treebody"
            rootName="All contexts"
            filterName="Filter by contexts"
            :itemsTree="contextOptions"
            :value="dataOptions.contexts"
            :applyFilter="dataOptions.filterContexts"
            @input="updateAnalysis('contexts', $event, false)"
            @filterCheck="updateAnalysis('filterContexts', $event, false)"
          />
        </div>
        <b-field horizontal label="Interval">
          <b-input 
            :value="analysis.interval"
            @input="updateAnalysis('interval', $event, true)"
            type="text" 
            pattern="^[0-9]+[mhd]$" 
            size="is-small" />
        </b-field>    
        <b-field horizontal label="From">
          <b-datepicker          
            :first-day-of-week="1"
            size="is-small"
            :value="dataOptions.start ? new Date(dataOptions.start) : null"
            @input="updateAnalysis('start', $event, false)">
            <button class="button is-primary is-small"
                @click="updateAnalysis('start', new Date(), false)">
                <b-icon icon="calendar-today" size="is-small"></b-icon>
                <span>Today</span>
            </button>
            <button class="button is-danger is-small"
                @click="updateAnalysis('start', null, false)">
                <b-icon icon="close-thick" size="is-small"></b-icon>
                <span>Clear</span>
            </button>
          </b-datepicker>
        </b-field>
         <b-field horizontal label="To">
          <b-datepicker          
            :first-day-of-week="1"
            size="is-small"
            :value="dataOptions.end ? new Date(dataOptions.end) : null"
            @input="updateAnalysis('end', $event, false)">
            <button class="button is-primary is-small"
                @click="updateAnalysis('end', new Date(), false)">
                <b-icon icon="calendar-today" size="is-small"></b-icon>
                <span>Today</span>
            </button>
            <button class="button is-danger is-small"
                @click="updateAnalysis('end', null, false)">
                <b-icon icon="close-thick" size="is-small"></b-icon>
                <span>Clear</span>
            </button>
          </b-datepicker>
        </b-field>      
      </div>
    </div>
  </b-collapse>
</div>  
</template>


<script>
import TreeSelect from '@/components/inputs/TreeSelect.vue';
import SearchSelect from '@/components/inputs/SearchSelect.vue';

export default {
  components:  { TreeSelect, SearchSelect },
  props: {
    index: {
      type: Number,
      default: 0,
    },
    analysis: {
      type: Object,
      default: () => {return {}}
    },
    allClients: {
      type: Array,
      default: () => []
    },
    tagOptions: {
      type: Array,
      default: () => []
    },
    contextOptions: {
      type: Array,
      default: () => []
    }
  },
  inject: {
    sharedState: {
      name: 'sharedState',
      default: {}
    }
  },
  data() {
    return {
      showDelete: false,     
    }
  },
  computed: {
    dataOptions() {
      return this.analysis.data_options[this.index]
    },
    inputNumber() {
      return this.index + 1
    },
    isOpen() {
      return this.sharedState.openNode === this.inputNumber.toString()
    },
  },
  methods: {
    updateAnalysis(prop, value, shared) {
      const isUpdatingToSameClient = (prop == 'client' && value == this.client)
      if (!isUpdatingToSameClient) {
        this.$emit('update', { prop: prop, value: value, index: this.index, shared: shared })
      } 
    },
    deleteInput() {
      this.$emit('delete', this.index)
    }
  },
} 

</script>


<style scoped>
.filters-box {
  max-height: 15rem;
  overflow: auto;
}

.treebody {
  flex-basis: 0;
  flex-grow: 5;
  flex-shrink: 1;
}
</style>