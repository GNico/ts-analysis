<template>

<div class="columns">
  <div class="column is-5">
    <b-table 
      v-if="!isEmpty"
      :data="anomalies" 
      :selected="selected"
      hoverable
      narrowed
      checkable
      @select="changeActiveAnomaly($event)">

      <template slot-scope="props">
        <b-table-column field="score" label="Score" numeric>
            {{ props.row.score }}
        </b-table-column>

        <b-table-column field="from" label="Start date" centered>
          {{ new Date(props.row.from).toLocaleString('es-AR', {month: '2-digit', day: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit'}) }}      
        </b-table-column>
        
        <b-table-column field="to" label="End date" centered>
          {{ new Date(props.row.to).toLocaleString('es-AR', {month: '2-digit', day: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit'}) }}
        </b-table-column>
      </template>
      
    </b-table>
  </div>
  <div class="column">
    {{ selected }}
  </div>
</div>

</template>


<script>


export default {
  computed: {
    anomalies() {
      return this.$store.getters['analysis/getDisplayAnomalies']
    },
    activeAnomaly() {
      return this.$store.state.analysis.activeAnomaly
    },
    selected() {
      return this.$store.getters['analysis/getAnomalyById'](this.activeAnomaly)
    },
    isEmpty() {
      return (!this.anomalies || !this.anomalies.length)
    }
  },
  methods: {
    changeActiveAnomaly(event) {
      this.$store.dispatch('analysis/setActiveAnomaly', event.id)
    }
  }
}


</script>