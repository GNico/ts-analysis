<template>
<b-table 
  ref="table"
  :data="filteredIncidents" 
  sticky-header      
  :selected="selected"
  checkable
  checkbox-position="right"
  hoverable
  @cellclick="openIncident"
  :default-sort="['monitor', 'asc']"
  :custom-is-checked="(a,b)=> a.id === b.id"
  :checked-rows="checked"
  @check="$emit('update:checked', $event)"
  @select="autoselected = $event">

  <b-table-column 
    field="" 
    sortable 
    label="Seen"  
    cell-class="is-unselectable"
  >
    <template v-slot:header="{ column }">
      <b-tooltip :label="column.label" append-to-body>
        <b-icon icon="eye-outline"/>
      </b-tooltip>
    </template>
    <template v-slot="props">
      <button class="transparent-button eye-button" @click="$emit('seenChange', {id: props.row.id, seen: !props.row.seen})">
        <b-icon 
          :icon="props.row.seen ? 'eye-check-outline' : 'eye-off-outline'" 
          :type="props.row.seen ? 'is-success' : 'is-primary'"></b-icon>
      </button>
    </template>      
  </b-table-column>

  <b-table-column 
    field="state" 
    label="State"  
    width="5%" 
    sortable 
    v-slot="props"  
    cell-class="is-unselectable"
    centered
  >    
    <b-dropdown :value="props.row.state" @input="$emit('stateChange', {id: props.row.id, state: $event})">
      <template #trigger>
        <span
          class="tag is-small is-clickable"
          :class="props.row.state == 'Open' ? 'is-success' : 'is-danger'" 
          size="is-small">     
          {{props.row.state}} &nbsp; <b-icon icon="menu-down" size="is-small"/>        
        </span>
      </template>
      <b-dropdown-item value="Open" aria-role="listitem">
        <span>Open</span>
      </b-dropdown-item>
      <b-dropdown-item value="Closed" aria-role="listitem">
        <span>Closed</span>
      </b-dropdown-item>                   
    </b-dropdown>
  </b-table-column>  
  <b-table-column 
    field="client" 
    label="Client" 
    width="20%" 
    sortable 
    v-slot="props"  
    cell-class="is-clickable is-unselectable"
  >
    {{ props.row.client }}       
  </b-table-column>  
  <b-table-column 
    field="monitor" 
    label="Monitor name"
    width="20%" 
    sortable
    v-slot="props"  
    cell-class="is-clickable is-unselectable">
    {{ props.row.monitor }}       
  </b-table-column>
  <b-table-column
    field="detector" 
    label="Detector name" 
    width="20%" 
    sortable 
    v-slot="props"  
    cell-class="is-clickable is-unselectable"
  >
    {{ props.row.analysis_name }}       
  </b-table-column>
  <b-table-column 
    field="start" 
    label="Start" 
    sortable 
    v-slot="props" 
    centered 
    cell-class="is-clickable is-unselectable"
  >
    {{ formatDateVerbose(props.row.start) }}
  </b-table-column>
  <b-table-column 
    :custom-sort="sortDuration" 
    label="Duration" 
    sortable 
    v-slot="props" 
    centered 
    cell-class="is-clickable is-unselectable"
  >
    {{ getDurationStr(props.row.start, props.row.end) }}
  </b-table-column>
  <b-table-column 
    field="score" 
    label="Score" 
    width="5%" 
    sortable 
    v-slot="props"  
    cell-class="is-clickable is-unselectable"
  >
    <span class="tag is-small" :style="getScoreTagStyle(props.row.score)">
      {{ parseFloat((props.row.score * 100).toFixed(1)) }}%
    </span>  
  </b-table-column>       
</b-table>
</template>


<script>
import api from '@/api/repository'
import { formatDateVerbose, timeRangeToString } from '@/utils/dateFormatter'

export default {
  components: {  },
  props: {
    allIncidents: {
      type: Array,
      default: () => []
    },
    searchValue: {
      type: String,
      default: ''
    },
    checked: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {      
      selected: undefined,
      autoselected: undefined,
    }
  },
  computed: {    
    filteredIncidents() {
      var term = this.searchValue.toLowerCase()
      return this.allIncidents.filter(elem => 
        elem.client.toLowerCase().includes(term) || 
        elem.monitor.toLowerCase().includes(term) ||
        elem.analysis_name.toLowerCase().includes(term))
    }
  },
  methods: {
    openIncident(incident, column, rowIndex, columnIndex) {
      if (columnIndex > 1) {
        this.selected = incident
        this.$emit('select', incident)      
      }
    },
    formatDateVerbose(date) {
      return formatDateVerbose(date)
    },
    getDurationStr(start, end) {
      var e = new Date(end)
      var s = new Date(start)     
      return timeRangeToString(e - s)
    },
    sortDuration(a, b, isAsc) {
      let dur1 = Date.parse(a.end) - Date.parse(a.start)
      let dur2 = Date.parse(b.end) - Date.parse(b.start)
      return isAsc ? dur1 < dur2 : dur1 > dur2
    },
    getScoreTagStyle(score) {
      if (score <= 0.33) {
        return { 'background-color': 'dodgerblue', color: 'white', 'font-weight': 600}
      } else if (score <= 0.66) {
        return { 'background-color': 'royalblue', color: 'white', 'font-weight': 600}
      } else {
        return { 'background-color': '#005aff', color: 'white', 'font-weight': 600}
      }
    },
    next() {
      this.$refs.table.pressedArrow(1)
      this.selected = this.autoselected
      this.$emit('select', this.selected) 
   
    },
    previous() {
      this.$refs.table.pressedArrow(-1)
      this.selected = this.autoselected
      this.$emit('select', this.selected) 
  
    },   
    
  },
 
}
</script>


<style scoped>
.button-right {
  border-left: 1px solid rgba(255,255,255,0.5);
}

.button-right:focus {
  border-left: 1px solid rgba(255,255,255,0.5);
}

.b-table .table th .th-wrap .icon {
  margin: 0;
}

.eye-button {
  padding: 0;
}
</style>