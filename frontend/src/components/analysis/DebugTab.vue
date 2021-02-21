<template>

<div>
  <b-field horizontal label="Select node">
    <b-select size="is-small" placeholder="Select a name">
      <option
        v-for="id in debugNodesNames"
        :value="id"
        :key="id">
        {{ id }}
      </option>
    </b-select>
  </b-field>
</div>

</template>



<script>

export default {

  data() {
    return {
      selectedNodeId: ''
    }
  },

  computed: {
    id() {
      return this.$store.state.analysis.activeAnalysisId
    },
    analysis() {
      return this.$store.getters['analysis/activeAnalysis']
    },
    model() {
      return this.analysis.model
    },
    results() {
      return this.$store.getters['analysis/activeResults'] 
    },
    loading() {
      return this.results.loading
    },
    debugNodes() {
      return !this.loading && this.results.hasOwnProperty("debug_nodes") ? this.results.debug_nodes :  {}
    },
    debugNodesNames() {
      return Object.keys(this.debugNodes)
    }
  }

}

</script>



