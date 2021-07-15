<template>
<div v-if="result.anomalies && result.anomalies.length" class="is-flex is-flex-direction-column" :style="{height: '400px'}">
  <div class="mb-2 has-text-white">
    <div> <strong class="has-text-white"> Anomalies</strong></div>
  </div>

  <AnomaliesTable   
    class="is-flex-grow-1"
    :anomalies="result.anomalies"
    :activeAnomaly="activeAnomalyId"
    @changeActive="$emit('changeActive', $event)"
  /> 
</div>

</template>


<script>
import AnomaliesTable from '@/components/analysis/AnomaliesTable'

export default {
  components: { AnomaliesTable },
  props: {
    result: {
      type: Object,
      default: () => {return {}} 
    },
    activeAnomalyId: {
      type: String,
      default: ''
    }
  },
  data() {
    return {

    }
  }

}

</script>