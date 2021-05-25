<template>
<div class="p-5">

  <IncidentWindow :incident="selectedIncident">
  </IncidentWindow>

  <IncidentsTable @select="onSelected"/>
</div>
</template>

<script>
import IncidentsTable from '@/components/monitoring/IncidentsTable'
import IncidentWindow from '@/components/monitoring/IncidentWindow'
import api from '@/api/repository'


export default {
  components: { IncidentsTable, IncidentWindow },
  data() {
    return {
      selectedIncident: {} 
    }
  },
  methods: {
    onSelected(incident) {
      api.getIncidentDetails(incident.id)
      .then(response => {
        this.selectedIncident = { ...response.data }
      })
    }
  },
  created() {
  }
}

</script>

<style>

 

</style>