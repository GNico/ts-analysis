<template>
<div class="p-5">

  <IncidentWindow v-if="showIncident" 
    :incident="selectedIncident"
    @close="showIncident = false"/>
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
      selectedIncident: {},
      showIncident: false,
    }
  },
  methods: {
    onSelected(incident) {
      api.getIncidentDetails(incident.id)
      .then(response => {
        this.selectedIncident = { ...response.data }
        this.selectedIncident.monitor = incident.monitor
        this.selectedIncident.analysis_name = incident.analysis_name
        this.showIncident = true     
      })
    }
  },
  created() {
  }
}

</script>

<style>

 

</style>