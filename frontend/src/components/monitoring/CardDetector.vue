<template>
<div class="card my-5">
  <header class="card-header">
    <div class="card-header-title is-justify-content-space-between">
      <span>{{detector.analysis_details.client}}: {{detector.analysis_details.name}}</span>
      <div class="is-flex is-align-items-center">
        <div class="header-item"> {{detector.last_run_at}} </div>
        <div class="header-item clickable" @click="confirmDelete">                
          <span class="icon"> 
            <i class="mdi mdi-trash-can"></i>
          </span>
          Delete 
        </div>
        <b-switch 
          v-model="detector.active" 
          left-label 
          size="is-small" 
          type="is-success" 
          passive-type="is-danger" 
          :rounded="false">
          {{detector.active ? 'ONLINE' : 'OFFLINE'}}
        </b-switch>
      </div>
    </div>        
  </header>
  <div class="card-content">
    <b-tabs size="" type="is-boxed" vertical :animated="false">

      <!--DETECTOR SETTINGS-->
      <b-tab-item label="Detector settings">
        <div class="columns">
          <div class="column is-12-mobile is-10-desktop is-8-widescreen is-6-fullhd">
            <b-field horizontal label="Execution interval">   
            <!--  <template #label>
                Execution interval
                <b-tooltip type="is-info" label="Amount of time that passes between analysis executions">
                  <b-icon size="is-small" icon="help-circle-outline"></b-icon>
                </b-tooltip>
              </template>    -->       
              <b-input 
              v-model="options.time_interval"
              size="is-small" 
              class="shorter-field"
              type="text" 
              pattern="^[0-9]+[mhd]$"/>
            </b-field>                     
            <b-field horizontal label="Relevant period">
           <!--   <template #label>
                Relevant period
                <b-tooltip type="is-info" label="Incidents older than this parameter will be ignored">
                  <b-icon size="is-small" icon="help-circle-outline"></b-icon>
                </b-tooltip>
              </template> -->
              <b-input 
              size="is-small" 
              class="shorter-field"
              v-model="options.incidents_period"
              type="text" 
              pattern="^[0-9]+[mhd]$"/>
            </b-field>
            <b-field horizontal label="Notifications">
              <b-switch 
                v-model="options.alerts_enabled" 
                size="is-small" 
                type="is-primary" 
                passive-type="is-grey">
                {{options.alerts_enabled ? 'Enabled' : 'Disabled'}}
              </b-switch>
            </b-field>
            
            <b-field horizontal class="mt-5">
              <a class="button is-primary is-small has-text-weight-semibold" @click="updateOpts">
                Save changes
              </a>
            </b-field>                   
          </div>
        </div>
      </b-tab-item> 

      <!--ANALYSIS SETTINGS-->
      <b-tab-item label="Analysis settings">
        <div class="columns">
          <div class="column is-12-mobile is-10-desktop is-8-widescreen is-6-fullhd">
            <b-field horizontal label="Client">
              {{detector.analysis_details.client}}
            </b-field>
            <b-field horizontal label="Tags">
              some tags?
            </b-field>
            <b-field horizontal label="Contexts">
              some contexts?
            </b-field>
            <b-field horizontal label="Interval">
              {{detector.analysis_details.data_options.interval}}
            </b-field>
            <b-field horizontal label="Detection model">
              <a @click="showGraph(detector.analysis_details.model)">Show</a>
            </b-field>
            <b-field horizontal class="mt-5">
              <a class="button is-primary is-small has-text-weight-semibold" @click="editAnalysis">
                Edit settings
              </a>
            </b-field>                   
          </div>
        </div>
      </b-tab-item>

      <!--RESULTS-->
      <b-tab-item label="Results">                        
      </b-tab-item>
    </b-tabs>    
  </div>
</div> 
</template>

<script>
export default {
  props: {
    detector: {
      type: Object,
      default: () => { return {}}
    }
  },
  data() {
    return {
      options: {
        alerts_enabled: true,
        time_interval: undefined,
        incidents_period: undefined,
      }

    }
  },
  methods: {
    confirmDelete() {
      this.$buefy.dialog.confirm({
        title: 'Deleting Detector',
        message: 'Are you sure you want to <b>delete</b> this item? This action cannot be undone.',
        confirmText: 'Delete Detector',
        type: 'is-danger',
        scroll: 'keep',
        hasIcon: true,
        onConfirm: () => this.deleteItem()
      })
    },
    deleteItem() {
    // api.deletePeriodicAnalysis(this.detector.monitor, this.detector.id)
     // .then(response => {
        //this.fetchData(this.data.id)
      this.$emit('delete', this.detector.id)
    //  })
    }, 
    updateOpts() {
      this.$emit('update', this.options)
    },
    editAnalysis() {
      this.$emit('editAnalysis', this.detector.analysis)
      //should switch to analysis page
    },
    showGraph() {
      this.$emit('showGraph', this.detector.analysis_details.model)
     // this.modelModalActive = true
     // this.modelData = data
    }
  }
}

</script>


<style scoped>

.header-item {
  border-right: 1px solid;
  padding-right: 0.75rem;
  margin-right: 0.75rem;
}


.clickable {
  cursor: pointer;
  user-select: none;
}

</style>