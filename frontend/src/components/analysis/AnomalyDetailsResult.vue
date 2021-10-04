<template>
<div>
  <TagCountTable 
    :settings="tableSettings" 
    :compareTo="compareMode" 
    :selectionRange="compareSelectionRange"
    @compareChange="updateCompareMode"/>
</div>
</template>

<script>
import TagCountTable from '@/components/analysis/TagCountTable'

export default {
  components: { TagCountTable },
  props: {
    anomaly: {
      type: Object,
      default: {}
    },    
  },
  data() {
    return {
      activeResults: {}
    }
  },
  computed: {
    active() {
      return this.$store.getters['results/activeResults']
    },
    compareMode() {
      return this.$store.state.results.compareTagsTo
    },
    compareSelectionRange() {
      return this.$store.state.results.compareSelection
    },
    tableSettings() {
      return {
        client: this.activeResults.settings.client, 
        data_options: this.activeResults.settings.data_options,
        anomalyStart: new Date(this.anomaly.from).toISOString(),
        anomalyEnd: new Date(this.anomaly.to).toISOString(), 
      }
    }
  },
  methods: {
    updateCompareMode(event) {
      this.$store.dispatch('results/updateCompareMode', event)
    }
  },
  watch: {    
  },
  created() {
    this.activeResults = this.$store.getters['results/activeResults']
  },  
}

</script>


<style>

</style>