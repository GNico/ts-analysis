<template>
<div class="p-5">
  <IncidentWindow 
    v-if="showIncident" 
    :incident="selectedIncident"
    @close="showIncident = false"
    @next="next"
    @previous="previous"
    @stateChange="updateIncident"
    @seenChange="updateIncident"
  />

  <div class="columns is-marginless mb-4">
    <div class="column is-6-mobile is-5-widescreen is-4-fullhd  is-paddingless">
      <b-field grouped>
        <b-input v-model="searchValue" expanded placeholder="Search..." size="is-small"/>        
        <IncidentsFilters @apply="filterData"/>
      </b-field>
    </div>
    <div class="column is-paddingless">
      <div class="is-flex is-align-items-center has-text-right is-justify-content-flex-end">
        <span class="mr-2 is-unselectable">On selected<span v-if="checked.length"> ({{checked.length}})</span>:</span> 
        <div class="field has-addons">
          <p class="control">
            <a class="button is-small is-primary" @click="performAction" :disabled="!checked.length">{{currentAction}}</a>
          </p>
          <p class="control">
            <b-dropdown scrollable :max-height="200" aria-role="list" position="is-bottom-left">
              <template #trigger="{ active }">
                <b-button class="button-right is-shadowless" icon-left="menu-down" size="is-small" type="is-primary"/>
              </template>
              <b-dropdown-item 
                v-for="action in onSelectedActions" 
                :key="action"
                @click="currentAction = action"
                aria-role="listitem">
                {{action}}
              </b-dropdown-item>
            </b-dropdown>
          </p>
        </div>        
      </div> 
    </div>
  </div>
  <IncidentsTable 
    :allIncidents="allIncidents"
    :searchValue="searchValue"
    :checked.sync="checked"
    @select="onSelected" 
    @stateChange="updateIncident"
    @seenChange="updateIncident"
    ref="table"/>
</div>
</template>

<script>
import IncidentsTable from '@/components/monitoring/IncidentsTable'
import IncidentWindow from '@/components/monitoring/IncidentWindow'
import api from '@/api/repository'
import IncidentsFilters from '@/components/monitoring/IncidentsFilters'


export default {
  components: { IncidentsTable, IncidentWindow, IncidentsFilters },
  data() {
    return {
      allIncidents: [],
      incidentsFilters: {},
      selectedIncident: {},
      showIncident: false,
      error: '',
      checked: [],
      currentAction: 'Mark as closed',
      onSelectedActions: [
        'Mark as closed',
        'Mark as open',
        'Mark as seen',
        'Mark as unseen',
        'Delete incident',       
      ],
      searchValue: '',
    }
  },
  computed: {
    checkedIds() {
      return this.checked.map(elem => elem.id)
    },
  },
  methods: {
    onSelected(incident) {
      api.getIncidentDetails(incident.id)
      .then(response => {
        this.selectedIncident = { ...response.data }
        this.selectedIncident.monitor = incident.monitor
        this.showIncident = true    
      })
    },
    next() {
      this.$refs.table.next()
    },
    previous() {
      this.$refs.table.previous()
    },
    updateIncident(event) {
      const {id, ...options} = event
      api.updateIncident(id, options)
      .then(response => {
        this.selectedIncident.state = response.data.state
        this.selectedIncident.seen = response.data.seen
        var found = this.allIncidents.find(elem => elem.id == id)
        if (found) {
          found.seen = this.selectedIncident.seen
          found.state = this.selectedIncident.state
        }
      })
    },
    fetchIncidents() {
      return  api.getAllIncidents(this.incidentsFilters)
              .then(response => {
                this.error = ''
                this.allIncidents = response.data
              })
              .catch(error => this.error = 'There was an error retrieving data')
    },
    performAction() {
      if (!this.checked.length) return
      switch (this.currentAction) {
        case this.onSelectedActions[0]: //mark closed
          api.updateIncidentsList(this.checkedIds, {state: 'Closed'})
          .then(response => this.fetchIncidents())
          break;      
        case this.onSelectedActions[1]: //mark open
          api.updateIncidentsList(this.checkedIds, {state: 'Open'})
          .then(response => this.fetchIncidents())
          break;
        case this.onSelectedActions[2]: //mark seen
          api.updateIncidentsList(this.checkedIds, {seen: true})
          .then(response => this.fetchIncidents())
          break;
        case this.onSelectedActions[3]: //mark unseen
          api.updateIncidentsList(this.checkedIds, {seen: false})
          .then(response => this.fetchIncidents())
          break; 
        case this.onSelectedActions[4]: //delete
          this.confirmDelete()
          break;        
      }
    },
    filterData(filters) {
      this.incidentsFilters = filters
      this.fetchIncidents()
    },
    confirmDelete() {
      this.$buefy.dialog.confirm({
        title: 'Deleting Incident',
        message: 'Are you sure you want to <b>delete</b> this items? This action cannot be undone.',
        confirmText: 'Delete Incident',
        type: 'is-danger',
        scroll: 'keep',
        hasIcon: true,
        onConfirm: () => api.deleteIncidentsList(this.checkedIds).then(response => {
          this.fetchIncidents()
        })
      })
    },
  },
  created() {
    this.fetchIncidents()
  }
}

</script>

<style>

 

</style>