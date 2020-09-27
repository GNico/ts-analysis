<template>

<div>
    <b-table 
      v-if="!isEmpty"
      :data="anomalies" 
      :selected="selected"
      hoverable
      narrowed
      @select="changeActiveAnomaly($event)">

      <template slot-scope="props">
        <b-table-column field="score" label="Score" sortable numeric>
            {{ props.row.score }}
        </b-table-column>

        <b-table-column field="from" label="Start date" sortable centered>
          {{ new Date(props.row.from).toLocaleString('es-AR', {month: '2-digit', day: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit'}) }}      
        </b-table-column>
        
        <b-table-column field="to" label="End date" sortable centered>
          {{ new Date(props.row.to).toLocaleString('es-AR', {month: '2-digit', day: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit'}) }}
        </b-table-column>
      </template>
      
    </b-table>
</div>
</template>

<script>


export default {
  props: {
    anomalies: {
      type: Array,
      default: []
    },
    activeAnomaly: {
      type: String,
    }
  },
  computed: {
    selected() {
      return this.anomalies.find(item => item.id === this.activeAnomaly)
    },
    isEmpty() {
      return (!this.anomalies || !this.anomalies.length)
    }
  },
  methods: {
    changeActiveAnomaly(event) {
      this.$emit('changeActive', event.id)
    }
  }
}


</script>