<template>
<div class="card my-5">
  <header class="card-header">
    <div class="card-header-title is-justify-content-space-between">
      <div class="is-flex is-vcentered clickable highlightable" @click="expanded = !expanded">
        <b-icon class="minimize-icon" :icon="!expanded ? 'menu-right' : 'menu-down'" size="is-default" ></b-icon>
        <span>&nbsp;{{detector.analysis_details.client}}: {{detector.analysis_details.name}}</span>
      </div>
      <div class="is-flex is-align-items-center">
        <div class="header-item"> {{detector.last_run_at}} </div>
        <div class="header-item clickable" @click="confirmDelete">                
          <span class="icon"> 
            <i class="mdi mdi-trash-can"></i>
          </span>
          Delete 
        </div>
        <b-switch 
          v-model="active" 
          @input="updateActive"
          left-label 
          size="is-small" 
          type="is-success" 
          passive-type="is-danger" 
          :rounded="false">
          {{active ? 'ONLINE' : 'OFFLINE'}}
        </b-switch>
      </div>
    </div>        
  </header>
  <div class="card-content p-4" v-show="expanded">
    <b-tabs 
      type="is-boxed"        
      :animated="false"
      destroy-on-hide>

      <!--DETECTOR SETTINGS-->
      <b-tab-item label="Settings">
        <div class="columns">   
          <div class="column is-8-mobile is-6-desktop is-5-widescreen is-3-fullhd">
            <div class="is-flex mb-3">
              <div class="has-text-grey-lighter has-text-weight-bold field-label is-normal">
                Execution frequency 
                <b-tooltip type="is-info" label="Amount of time that passes between analysis executions">
                  <b-icon size="is-small" icon="help-circle-outline"></b-icon>
                </b-tooltip>
              </div>  
              <b-input 
                v-model="options.time_interval"
                size="is-small" 
                class="shorter-field"
                type="text" 
                pattern="^[0-9]+[mhd]$"/>   
            </div> 

            <div class="is-flex mb-3">
              <div class="has-text-grey-lighter has-text-weight-bold field-label is-normal">
                Data time window
                <b-tooltip type="is-info" label="Data prior to this period will not be taken into account">
                  <b-icon size="is-small" icon="help-circle-outline"></b-icon>
                </b-tooltip>
              </div>  
              <b-input 
                size="is-small" 
                class="shorter-field"
                v-model="options.data_time_window"
                type="text" 
                pattern="^[0-9]+[mhd]$"/>   
            </div> 

            <div class="is-flex mb-3">
              <div class="has-text-grey-lighter has-text-weight-bold field-label is-normal">
                Anomaly time window
                <b-tooltip type="is-info" label="Anomalies prior to this period will not be taken into account">
                  <b-icon size="is-small" icon="help-circle-outline"></b-icon>
                </b-tooltip>
              </div>  
              <b-input 
                size="is-small" 
                class="shorter-field"
                v-model="options.anomaly_time_window"
                type="text" 
                pattern="^[0-9]+[mhd]$"/>   
            </div>

            <div class="is-flex mb-3 ml-5">
              <div class="has-text-grey-lighter has-text-weight-bold field-label">
                Notifications               
              </div>  
              <b-switch
                class="shorter-field"
                v-model="options.alerts_enabled" 
                :rounded="false"
                type="is-primary" 
                passive-type="is-grey">
                {{options.alerts_enabled ? 'Enabled' : 'Disabled'}}
              </b-switch>   
            </div>   

            <div class="is-flex mt-5 is-justify-content-flex-end">
              <a class="button is-primary is-small has-text-weight-semibold" @click="updateOpts">
                Save changes
              </a>
            </div>                

          </div>
        </div>
      </b-tab-item> 

      <!--ANALYSIS SETTINGS-->
      <b-tab-item label="Detection model">
        <CardDetectorModelTab :analysisDetails="detector.analysis_details"/>                
      </b-tab-item>

      <!--RESULTS-->
      <b-tab-item label="Results">                        
      </b-tab-item>
    </b-tabs>    
  </div>
</div> 
</template>

<script>
import debounce from "lodash/debounce"
import CardDetectorModelTab from '@/components/monitoring/CardDetectorModelTab'

export default {
  components: { CardDetectorModelTab },
  props: {
    detector: {
      type: Object,
      default: () => { return {}}
    }
  },
  data() {
    return {
      expanded: false,
      active: undefined,
      options: {
        alerts_enabled: undefined,
        time_interval: undefined,
        relevant_period: undefined,
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
      this.$emit('delete', this.detector.id)
    }, 
    updateOpts() {
      this.$emit('update', this.options)
    },
    updateActive() {
      this.$emit('update', {active: this.active})
    },
    editAnalysis() {
      this.$emit('editAnalysis', this.detector.analysis)
    },
  },
  watch: {
    detector: {
      deep: true,
      immediate: true,
      handler(newOpts) {
        this.active = newOpts.active
        Object.keys(this.options).forEach(key => {
          if (newOpts.hasOwnProperty(key) && this.options[key] !== newOpts[key]) {
            this.options[key] = newOpts[key] 
          }
        })
      }
    }
  },
  created() {
    this.updateActive = debounce(this.updateActive, 400)
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

.highlightable:hover {
  filter: brightness(200%);
}

</style>