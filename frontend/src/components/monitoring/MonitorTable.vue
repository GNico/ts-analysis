<template>
  <div class="p-5"> 
    
    <div class="is-flex is-justify-content-space-between mb-5">
      <b-input placeholder="Search"> </b-input>


      <b-dropdown ref="dropdown" position="is-bottom-left" append-to-body trap-focus>
        <a
          class="button is-primary"
          slot="trigger"
          role="button">
          <b-icon  icon="playlist-plus"></b-icon>
          <span class="has-text-weight-semibold">New Monitor</span>
        </a>
        <b-dropdown-item
          aria-role="menu-item"
          :focusable="false"
          custom
          paddingless>
          <FormNewMonitor @submit="addMonitor" :loading="creatingMonitor"/>
        </b-dropdown-item>
      </b-dropdown>

     
    </div>

      

    <b-table 
      :data="allMonitors" 
      sticky-header      
      selectable
      hoverable
      @cellclick="openMonitor"
      :default-sort="['name', 'asc']">

      <b-table-column field="name" label="Monitor" sortable v-slot="props" width="50%" cell-class="is-clickable">
        {{ props.row.name }}       
      </b-table-column>
      <b-table-column field="detectors" label="Detectors" sortable v-slot="props" numeric cell-class="is-clickable">
        {{ props.row.detectors }}       
      </b-table-column>
      <b-table-column field="incidents" label="Open incidents" sortable v-slot="props" numeric cell-class="is-clickable">
        {{ props.row.incidents }}       
      </b-table-column>
      <b-table-column field="last_incident" label="Last incident" v-slot="props"  width="20%" centered cell-class="is-clickable">
        {{ props.row.last_incident }}
      </b-table-column>

      <b-table-column field="delete" label="" v-slot="props" centered>
        <button class="transparent-button" @click="deleteMonitor(props.row.id)">
          <b-icon icon="trash-can" type="is-grey"></b-icon>
        </button>
      </b-table-column>
    
    </b-table>
  </div>
</template>

<script>
import api from '@/api/repository'
import { formatDate } from '@/utils/helpers'
import FormNewMonitor from '@/components/monitoring/FormNewMonitor'

export default {
  components: { FormNewMonitor },
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

      creatingMonitor: false,

    }
  },
  computed: {   
    savedAnalysis() {
      return this.$store.state.analysis.all
    },
  },
  methods: {
    fetchMonitors() {
      return  api.getAllMonitors()
              .then(response => {
                this.error = ''
                this.allMonitors = response.data
              })
              .catch(error => this.error = 'There was an error retrieving data')
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
    addMonitor(form) {
      this.creatingMonitor = true
      api.addNewMonitor(form.name)
      .then(response => {
        this.creatingMonitor = false
        this.$router.push({ name: 'MonitorDetails', params: {id: response.data.id }})
      })
      .catch(error => {
        this.creatingMonitor = false
        this.$refs.dropdown.isActive = false
        this.$buefy.toast.open({
          message: 'An error occurred',
          type: 'is-danger',
          duration: 2500,
        })
      })     
    },    
    deleteMonitor(id) {
      api.deleteMonitor(id)
      .then(this.fetchMonitors)     
    },    
    openMonitor(row, column, rowIndex, columnIndex ) {
      //warning: hardcoded last row
      if (columnIndex != 4) {    
        this.$router.push({ name: 'MonitorDetails', params: {id: row.id}}) 
      }
    },
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