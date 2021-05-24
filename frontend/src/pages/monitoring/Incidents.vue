<template>
<div class="p-5">
  <IncidentsTable/>
</div>
</template>

<script>
import IncidentsTable from '@/components/monitoring/IncidentsTable'
import api from '@/api/repository'


export default {
  components: { IncidentsTable },
  data() {
    return {
      
    }
  },
  methods: {
    
  },
  created() {
  }
}

</script>

<style>

</style>
