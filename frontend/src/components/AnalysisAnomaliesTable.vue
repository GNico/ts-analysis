<template>

<div>
    <b-table 
      v-if="!isEmpty"
      :data="anomalies" 
      :selected="selected"
      hoverable
      narrowed
      sticky-header
      :height="height"
      @select="changeActiveAnomaly($event)">

      <template slot-scope="props">
        <b-table-column field="score" label="Score" sortable numeric id="pija">
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
      default: () => { return [] }
    },
    activeAnomaly: {
      type: String,
    },
    height: {
      type: [ Number, String ],
      default: 250,
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