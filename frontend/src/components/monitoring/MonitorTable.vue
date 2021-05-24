<template>
  <div class="p-5"> 
    <div class="columns is-marginless mb-4">
      <div class="column is-6-mobile is-5-widescreen is-4-fullhd  is-paddingless">
        <b-input expanded placeholder="Search..." size="is-small"></b-input>        
      </div>

      <div class="column is-paddingless">
        <div class="is-flex is-align-items-center has-text-right is-justify-content-flex-end">
          <b-dropdown ref="dropdown" position="is-bottom-left" append-to-body trap-focus>
            <a
              class="button is-primary is-small"
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
      </div>
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
        {{ props.row.num_detectors }}       
      </b-table-column>
      <b-table-column field="incidents" label="Open incidents" sortable v-slot="props" numeric cell-class="is-clickable">
        {{ props.row.num_incidents }}       
      </b-table-column>
      <b-table-column field="last_incident" label="Last incident" sortable v-slot="props"  width="20%" centered cell-class="is-clickable">
        {{ formatDate(props.row.last_incident) }}
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
import { formatDateVerbose } from '@/utils/helpers'
import FormNewMonitor from '@/components/monitoring/FormNewMonitor'

export default {
  components: { FormNewMonitor },
  data() {
    return {
      allMonitors: [],
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
      return formatDateVerbose(input)
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
      //warning: hardcoded last row index
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