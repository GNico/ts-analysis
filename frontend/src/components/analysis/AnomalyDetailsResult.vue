<template>
<div>
  <TagCountTable :settings="tableSettings"/>
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