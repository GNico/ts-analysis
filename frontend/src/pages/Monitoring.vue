<template>
<div class="container section"> 
  <div v-if="error" class="is-size-5 has-text-centered"> {{ error }} </div>
  <template v-else>
    <div class="selected-action has-text-right">
      <span class="selected-label">On selected:</span> 
      <a class="button is-small is-primary button-left" @click="performAction">{{currentAction}}</a>
      <b-dropdown scrollable :max-height="200" aria-role="list" position="is-bottom-left">
        <template #trigger="{ active }">
          <b-button class="button-right" icon-left="menu-down" size="is-small" type="is-primary"/>
        </template>

        <b-dropdown-item 
          v-for="action in onSelectedActions" 
          :key="action"
          @click="currentAction = action"
          aria-role="listitem">
          {{action}}
        </b-dropdown-item>
      </b-dropdown>
    </div> 

    <b-table 
      :data="allPeriodicAnalysis" 
      sticky-header
      checkbox-position="right"
      checkable
      selectable
      detailed
      :opened-detailed="openRows"
      detail-key="analysis"
      @details-open="addRowDetails"
      :default-sort="['client', 'asc']"
      :custom-is-checked="(a,b)=> a.analysis === b.analysis"
      :checked-rows.sync="checked">
      <template slot-scope="props">  
        <b-table-column field="client" label="Client" sortable  >
          {{ props.row.client }}       
        </b-table-column>
        <b-table-column field="name" label="Analysis Name" sortable >
          {{ props.row.name }}      
        </b-table-column>
        <b-table-column field="description" label="Analysis Description" >
          {{ props.row.description }}       
        </b-table-column>
        <b-table-column field="monitoring" label="Monitoring">
          <span v-if="props.row.active" class="tag is-success""> Active </span>
          <span v-else class="tag is-warning""> Disabled </span>
        </b-table-column>
        <b-table-column field="alerts" label="Alerts">
          <span v-if="props.row.alerts_enabled" class="tag is-success""> Enabled </span>
          <span v-else class="tag is-warning""> Disabled </span>
        </b-table-column>
        <b-table-column field="last_run" label="Last run">
           {{ formatDate(props.row.last_run_at) }}
        </b-table-column>
      </template>

      <template #detail="props">
        <TableDetails :details="rowDetails[props.row.analysis]" @update="updateOptions(props.row.analysis, $event)"/>
      </template>
    </b-table>
  </template>
</div>
</template>

<script>
import TableDetails from '../components/monitoring/TableDetails'
import api from '../api/repository'
import { formatDate } from '../utils/helpers'

export default {
  components: { TableDetails },
  data() {
    return {
      checked: [],     
      openRows: [],   
      rowDetails: {},
      allPeriodicAnalysis: [],
      error: '',
      currentAction: 'Delete Analysis',
      onSelectedActions: [
        'Delete Analysis',
        'Activate Monitoring',
        'Disable Monitoring',
        'Activate Alerts',
        'Turn off Alerts'
      ]
    }
  },
  computed: {
    checkedIds() {
      return this.checked.map(elem => elem.analysis)
    },
  },
  methods: {
    fetchPeriodicAnalysis() {
      return  api.getAllPeriodicAnalysis()
              .then(response => {
                this.error = ''
                this.allPeriodicAnalysis = response.data
              })
              .catch(error => this.error = 'There was an error retrieving data')
    },
    formatDate(input) {
      return formatDate(input)
    },
    confirmDelete() {
      this.$buefy.dialog.confirm({
        title: 'Deleting Analysis',
        message: 'Are you sure you want to <b>delete</b> this items? This action cannot be undone.',
        confirmText: 'Delete Analysis',
        type: 'is-danger',
        scroll: 'keep',
        hasIcon: true,
        onConfirm: () => this.$store.dispatch('analysis/deleteAnalysisList', this.checkedIds).then(response => this.fetchPeriodicAnalysis())
      })
    },
    performAction() {
      if (!this.checked.length) return
      switch (this.currentAction) {
        case this.onSelectedActions[0]: //delete
          this.confirmDelete()
          break;
        case this.onSelectedActions[1]: //activate monitoring
          api.updatePeriodicAnalysisList(this.checkedIds, {active: true})
          .then(response => this.fetchPeriodicAnalysis())
          break;
        case this.onSelectedActions[2]: //disable monitoring
          api.updatePeriodicAnalysisList(this.checkedIds, {active: false})
          .then(response => this.fetchPeriodicAnalysis())
          break;
        case this.onSelectedActions[3]: //activate alerts
          api.updatePeriodicAnalysisList(this.checkedIds, {alerts_enabled: true})
          .then(response => this.fetchPeriodicAnalysis())
          break;
        case this.onSelectedActions[4]: //disable alerts
          api.updatePeriodicAnalysisList(this.checkedIds, {alerts_enabled: false})
          .then(response => this.fetchPeriodicAnalysis())
          break; 
      }
    },
    addRowDetails(row) {
      api.getPeriodicAnalysis(row.analysis)
      .then(response => {
        this.rowDetails = {...this.rowDetails, [row.analysis]: response.data}
      })    
    },
    updateOptions(id, options) {
      api.updatePeriodicAnalysis(id, options)
      .then(response => {
        let index = this.allPeriodicAnalysis.findIndex(elem => elem.analysis == id)
        if (index != -1) {
          this.allPeriodicAnalysis.splice(index, 1, response.data )
        }
      })
    },
  },
  created() {
    this.fetchPeriodicAnalysis()
  }
}
</script>


<style scoped>
.selected-action {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  margin-bottom: 0.75rem;
}

.selected-label {
  margin-right: 0.5rem;
}

.button-left {
  border-radius: 3px 0 0 3px;
}

.button-right {
  border-radius: 0 3px 3px 0;
  border-left: 1px solid rgba(255,255,255,0.5);
}
</style>