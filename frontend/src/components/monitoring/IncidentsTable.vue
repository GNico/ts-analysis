<template>
  <b-table 
    :data="incidents" 
    sticky-header      
    selectable
    checkable
    checkbox-position="right"
    hoverable
    @cellclick="openIncident"
    :default-sort="['name', 'asc']">

    <b-table-column field="state" label="State"  width="5%" sortable v-slot="props"  cell-class="is-clickable">
      {{ props.row.state }}       
    </b-table-column>
    <b-table-column field="score" label="Score" width="5%" sortable v-slot="props"  cell-class="is-clickable">
      {{ props.row.score }}       
    </b-table-column>
    <b-table-column field="monitor" label="Monitor name" sortable v-slot="props"  cell-class="is-clickable">
      {{ props.row.monitor }}       
    </b-table-column>
    <b-table-column field="detector" label="Detector name" sortable v-slot="props"  cell-class="is-clickable">
      {{ props.row.analysis_name }}       
    </b-table-column>
    <b-table-column field="start" label="Start" v-slot="props" centered cell-class="is-clickable">
      {{ formatDate(props.row.start) }}
    </b-table-column>
    <b-table-column field="end" label="End" v-slot="props" centered cell-class="is-clickable">
      {{ formatDate(props.row.end) }}
    </b-table-column>    

    
  </b-table>
</template>


<script>
import { formatDate } from '@/utils/helpers'

export default {
  props: {
    incidents: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
    }
  },
  methods: {
    openIncident() {
      console.log('open')
    },
    formatDate(date) {
      return formatDate(date)
    }
  }
}

</script>