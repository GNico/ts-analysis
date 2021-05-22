<template>
<div class="p-5">
  <IncidentsTable :incidents="allIncidents"/>
</div>
</template>

<script>
import IncidentsTable from '@/components/monitoring/IncidentsTable'
import api from '@/api/repository'


export default {
  components: { IncidentsTable },
  data() {
    return {
      allIncidents: [],
      error: ''
    }
  },
  methods: {
    fetchIncidents() {
      return  api.getAllIncidents()
              .then(response => {
                this.error = ''
                this.allIncidents = response.data
              })
              .catch(error => this.error = 'There was an error retrieving data')
    }
  },
  created() {
    this.fetchIncidents()
  }
}

</script>
