<template>
<div>
  <div class="columns is-marginless mb-4">
    <div class="column is-6-mobile is-5-widescreen is-4-fullhd  is-paddingless">
      <b-field grouped>
          <b-input expanded placeholder="Search..." size="is-small"></b-input>
          <p class="control">
            <a class="button is-primary is-small">
              <b-icon size="is-small" icon="filter-variant"></b-icon>
              <span class="has-text-weight-semibold">Filters</span>
            </a>
          </p>
      </b-field>
    </div>
    <div class="column is-paddingless">
      <div class="is-flex is-align-items-center has-text-right is-justify-content-flex-end">
        <span class="mr-2">On selected:</span> 
        <div class="field has-addons">
          <p class="control">
            <a class="button is-small is-primary" @click="performAction">{{currentAction}}</a>
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

  <b-table 
    :data="allIncidents" 
    sticky-header      
    selectable
    :selected.sync="selected"
    checkable
    checkbox-position="right"
    hoverable
    @cellclick="openIncident"
    :default-sort="['monitor', 'asc']"
    :custom-is-checked="(a,b)=> a.id === b.id"
    :checked-rows.sync="checked">

    <b-table-column field="state" label="State"  width="5%" sortable v-slot="props"  cell-class="is-clickable">
      <span class="tag is-small" :class="props.row.state=='Open' ? 'is-success' : 'is-warning'">{{ props.row.state }}</span>     
    </b-table-column>  
    <b-table-column field="client" label="Client" width="20%" sortable v-slot="props"  cell-class="is-clickable">
      {{ props.row.client }}       
    </b-table-column>  
    <b-table-column field="monitor" label="Monitor name" width="20%" sortable v-slot="props"  cell-class="is-clickable">
      {{ props.row.monitor }}       
    </b-table-column>
    <b-table-column field="detector" label="Detector name" width="20%" sortable v-slot="props"  cell-class="is-clickable">
      {{ props.row.analysis_name }}       
    </b-table-column>
    <b-table-column field="start" label="Start" sortable v-slot="props" centered cell-class="is-clickable">
      {{ formatDate(props.row.start) }}
    </b-table-column>
    <b-table-column field="end" label="End" sortable v-slot="props" centered cell-class="is-clickable">
      {{ formatDate(props.row.end) }}
    </b-table-column>
    <b-table-column field="score" label="Score" width="5%" sortable v-slot="props"  cell-class="is-clickable">
      <span>{{ props.row.score }}</span>     
    </b-table-column>       
  </b-table>
</div>
</template>


<script>
import api from '@/api/repository'
import { formatDate } from '@/utils/helpers'

export default {
  data() {
    return {
      allIncidents: [],
      checked: [],
      selected: undefined,
      error: '',
      currentAction: 'Mark as closed',
      onSelectedActions: [
        'Mark as closed',
        'Mark as open',
        'Delete incident',       
      ],
    }
  },
  computed: {
    checkedIds() {
      return this.checked.map(elem => elem.id)
    },
  },
  methods: {
    openIncident(incident) {
      this.$emit('select', incident)
    },
    formatDate(date) {
      return formatDate(date)
    },
    fetchIncidents() {
      return  api.getAllIncidents()
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
        case this.onSelectedActions[2]: //delete
          this.confirmDelete()
          break;        
      }
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


<style scoped>
.button-right {
  border-left: 1px solid rgba(255,255,255,0.5);
}

.button-right:focus {
  border-left: 1px solid rgba(255,255,255,0.5);
}
</style>