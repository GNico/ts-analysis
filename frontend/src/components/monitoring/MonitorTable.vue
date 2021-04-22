<template>
  <div class="p-5"> 
    
    <div class="is-flex is-justify-content-space-between mb-5">
      <b-input placeholder="Search"> </b-input>
      <a class="button is-primary">
        <b-icon icon="playlist-plus"></b-icon>
        <span class="has-text-weight-semibold">New monitor</span>
      </a>
    </div>

      

    <b-table 
      :data="allMonitors" 
      sticky-header      
      selectable
      hoverable
      @click="openMonitor"
      :default-sort="['name', 'asc']">

      <b-table-column field="name" label="Monitor" sortable v-slot="props" width="50%">
        {{ props.row.name }}       
      </b-table-column>
      <b-table-column field="detectors" label="Detectors" sortable v-slot="props" numeric>
        {{ props.row.detectors }}       
      </b-table-column>
      <b-table-column field="incidents" label="Open incidents" sortable v-slot="props" numeric>
        {{ props.row.incidents }}       
      </b-table-column>
      <b-table-column field="last_incident" label="Last incident" v-slot="props"  width="20%" centered>
        {{ props.row.last_incident }}
      </b-table-column>

      <b-table-column field="delete" label="" v-slot="props" centered>
        <b-icon icon="trash-can" size=""/>
      </b-table-column>
    
    </b-table>
  </div>
</template>

<script>
import api from '@/api/repository'
import { formatDate } from '@/utils/helpers'

export default {
  components: {  },
  data() {
    return {
      allMonitors: [{
        name: 'Pepega',
        detectors: 2,
        incidents: 0,
        last_incident: '20 Jun 2021, 12:45'
      },
      {
        name: 'Another',
        detectors: 23,
        incidents: 2,
        last_incident: '20 Jun 2021, 18:25'
      }],
      error: '',      
      loadModalActive: false,
    }
  },
  computed: {   
    savedAnalysis() {
      return this.$store.state.analysis.all
    },
  },
  methods: {
    fetchMonitors() {
  /*    return  api.getAllMonitors()
              .then(response => {
                this.error = ''
                this.allMonitors = response.data
              })
              .catch(error => this.error = 'There was an error retrieving data') */
    },
    formatDate(input) {
      return formatDate(input)
    },
    confirmDelete() {
      this.$buefy.dialog.confirm({
        title: 'Deleting Monitor',
        message: 'Are you sure you want to <b>delete</b> this items? This action cannot be undone.',
        confirmText: 'Delete Monitor',
        type: 'is-danger',
        scroll: 'keep',
        hasIcon: true,
        onConfirm: () => api.deletePeriodicAnalysisList(this.checkedIds).then(response => {
          this.fetchMonitors()
        })
      })
    },
    openMonitor(row) {
      this.$router.push({ name: 'MonitorDetails', params: {id: row.name}}) 
    },
   /* toggleRow(event) {
      let index = this.openRows.findIndex(elem => elem === event.analysis)
      if (index != -1) {
        this.openRows.splice(index, 1)
      } else {
        this.openRows.push(event.analysis)
        this.addRowDetails(event.analysis)
      }
    },
*/  updateOptions(id, options) {
      api.updatePeriodicAnalysis(id, options)
      .then(response => {
        let index = this.allPeriodicAnalysis.findIndex(elem => elem.analysis == id)
        if (index != -1) {
          this.allPeriodicAnalysis.splice(index, 1, response.data )
        }
      })
    },
 /*   addMonitor(id) {
      let index = this.allMonitors.findIndex(elem => elem.analysis == id)
      if (index != -1) {
        this.$buefy.toast.open({
          message: "Monitor already exists!",
          type: 'is-danger',
          duration: 2500,
        })
      } else {
        api.addNewPeriodicAnalysis(id)
        .then(response => {
          this.fetchPeriodicAnalysis()
          this.$buefy.toast.open({
            message: "Monitor created",
            type: 'is-success',
            duration: 2500,
          })
        })
        .catch(error => console.log(error))
      }      
    } */
  },
  created() {
    this.fetchMonitors()
  }
}
</script>


<style scoped>
.button-right {
  border-left: 1px solid rgba(255,255,255,0.5);
}

.button-right:focus {
  border-left: 1px solid rgba(255,255,255,0.5);
}
</style>