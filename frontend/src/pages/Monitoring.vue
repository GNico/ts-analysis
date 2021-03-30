<template>
<div class="container section"> 
  <ModalLoadAnalysis 
    :allAnalysis="savedAnalysis"
    :isActive="loadModalActive" 
    @close="loadModalActive = false"
    @load="addMonitor"
    title="Select Analysis"
    :allowDelete="false"
    confirmLabel="Create Monitor"
  />

  <div v-if="error" class="is-size-5 has-text-centered"> {{ error }} </div>
  <template v-else>
    <div class="is-flex is-align-items-center is-justify-content-space-between mb-3 ">
      <a class="button is-primary is-small" @click="loadModalActive = !loadModalActive">
        <b-icon  icon="playlist-plus"></b-icon>
        <span class="has-text-weight-semibold">New Monitor</span>
      </a>

      <div class="is-flex is-align-items-center has-text-right">
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

    <b-table 
      :data="allPeriodicAnalysis" 
      sticky-header
      checkbox-position="right"
      checkable
      selectable
      detailed
      :opened-detailed="openRows"
      detail-key="analysis"
      @details-open="addRowDetails($event.analysis)"
      @click="toggleRow"
      :default-sort="['client', 'asc']"
      :custom-is-checked="(a,b)=> a.analysis === b.analysis"
      :checked-rows.sync="checked">

      <b-table-column field="client" label="Client" sortable v-slot="props">
        {{ props.row.client }}       
      </b-table-column>
      <b-table-column field="name" label="Analysis Name" sortable v-slot="props">
        {{ props.row.name }}      
      </b-table-column>
      <b-table-column field="description" label="Analysis Description" v-slot="props">
        {{ props.row.description }}       
      </b-table-column>
      <b-table-column field="monitoring" label="Monitoring" v-slot="props">
        <span v-if="props.row.active" class="tag is-success""> Active </span>
        <span v-else class="tag is-warning""> Disabled </span>
      </b-table-column>
      <b-table-column field="alerts" label="Alerts" v-slot="props">
        <span v-if="props.row.alerts_enabled" class="tag is-success""> Enabled </span>
        <span v-else class="tag is-warning""> Disabled </span>
      </b-table-column>
      <b-table-column field="last_run" label="Last run" v-slot="props">
         {{ formatDate(props.row.last_run_at) }}
      </b-table-column>

      <template #detail="props">
        <TableDetails :details="rowDetails[props.row.analysis]" @update="updateOptions(props.row.analysis, $event)"/>
      </template>
    </b-table>
  </template>
</div>
</template>

<script>
import TableDetails from '../components/monitoring/TableDetails'
import ModalLoadAnalysis from "../components/analysis/ModalLoadAnalysis"
import api from '../api/repository'
import { formatDate } from '../utils/helpers'

export default {
  components: { TableDetails, ModalLoadAnalysis },
  data() {
    return {
      checked: [],     
      openRows: [],   
      rowDetails: {},
      allPeriodicAnalysis: [],
      error: '',
      currentAction: 'Delete Monitor',
      onSelectedActions: [
        'Delete Monitor',
        'Activate Monitor',
        'Disable Monitor',
        'Activate Alerts',
        'Turn off Alerts'
      ],
      loadModalActive: false,

    }
  },
  computed: {
    checkedIds() {
      return this.checked.map(elem => elem.analysis)
    },
    savedAnalysis() {
      return this.$store.state.analysis.all
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
        title: 'Deleting Monitor',
        message: 'Are you sure you want to <b>delete</b> this items? This action cannot be undone.',
        confirmText: 'Delete Monitor',
        type: 'is-danger',
        scroll: 'keep',
        hasIcon: true,
        onConfirm: () => api.deletePeriodicAnalysisList(this.checkedIds).then(response => {
          this.fetchPeriodicAnalysis()
        })
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
    addRowDetails(analysisId) {
      api.getPeriodicAnalysis(analysisId)
      .then(response => {
        this.rowDetails = {...this.rowDetails, [analysisId]: response.data}
      })    
    },
    toggleRow(event) {
      let index = this.openRows.findIndex(elem => elem === event.analysis)
      if (index != -1) {
        this.openRows.splice(index, 1)
      } else {
        this.openRows.push(event.analysis)
        this.addRowDetails(event.analysis)
      }
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
    addMonitor(id) {
      let index = this.allPeriodicAnalysis.findIndex(elem => elem.analysis == id)
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
    }
  },
  created() {
    this.fetchPeriodicAnalysis()
    this.$store.dispatch("analysis/fetchAllAnalysis")
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