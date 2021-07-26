<template>
<div class="p-5"> 
  <ModalLoadAnalysis 
    :allAnalysis="savedAnalysis"
    :isActive="loadModalActive" 
    @close="loadModalActive = false"
    @load="addItem"
    title="Select Analysis"
    :allowDelete="false"
    confirmLabel="Create Detector"/>
  
  <div class="title">{{ monitor.name }}</div>
  <b-tabs type="is-medium"  :animated="false"  destroy-on-hide>
    <b-tab-item label="Detectors" icon="alarm-light" value="Detectors">
      <div class="is-flex is-justify-content-space-between mb-2">
        <b-input placeholder="Search" size="is-small"> </b-input>
        <a class="button is-primary is-small" @click="loadModalActive = !loadModalActive">
          <b-icon icon="playlist-plus"></b-icon>
          <span class="has-text-weight-semibold">Add detector</span>
        </a>
      </div>
      
      <CardDetector 
        v-for="detector in monitor.detectors" 
        ref="cardDetector"
        :key="detector.id"
        :detector="detector"
        @delete="deleteItem"
        @update="updateOpts(detector.id, $event)"
        @editAnalysis="editAnalysis" />
    </b-tab-item>

    <b-tab-item label="Notification channels" icon="bell" value="Notifications">
      <MonitorNotifications 
        :emails="monitor.notification_channels"
        @add="addNotification"
        @delete="deleteNotification"/>
    </b-tab-item>
  </b-tabs>
</div>
</template>


<script>
import api from '@/api/repository'
import ModalLoadAnalysis from '@/components/analysis/ModalLoadAnalysis'
import CardDetector from './CardDetector'
import MonitorNotifications from './MonitorNotifications'

export default {
  components: { ModalLoadAnalysis, CardDetector, MonitorNotifications },
  data() {
    return {
      loadModalActive: false,
      loading: false,
      error: '',
      monitor: {},
      options: {
        alerts_enabled: true,
        time_interval: undefined,
        incidents_period: undefined,
      },
    }
  },
  computed: {
    savedAnalysis() {
      return this.$store.state.analysis.all
    },
  },
  methods: {
    fetchData(monitorId) {
      this.loading = true
      return  api.getMonitorDetails(monitorId)
              .then(response => {
                this.monitor = { ...response.data }
                console.log("monitor")
                console.log(this.monitor)
              })
    },
    addItem(id) {
      api.addNewPeriodicAnalysis(this.monitor.id, id)
      .then(response => {        
        this.fetchData(this.monitor.id).then(resp => {
          this.expandDetector(response.data.id)
        })
        this.$buefy.toast.open({
          message: "Detector created",
          type: 'is-success',
          duration: 2500,
        })    
      })
      .catch(error => console.log(error))
    },
    expandDetector(id) {
      this.$nextTick(() => {        
        var elem = this.$refs.cardDetector.find(c => c.detector.id == id)
        if (elem) elem.expanded = true         
      })
    },
    deleteItem(id) {
      api.deletePeriodicAnalysis(this.monitor.id, id)
      .then(response => {
        this.fetchData(this.monitor.id)
      })
    },
    updateOpts(id, options) {
      api.updatePeriodicAnalysis(this.monitor.id, id, options)
      .then(response => {
        this.fetchData(this.monitor.id)
      })
    },
    editAnalysis(analysis) {
      //should switch to analysis page
      console.log(analysis)
    },
    deleteNotification(id) {
      api.deleteNotificationChannel(id)
      .then(response => {
        this.fetchData(this.monitor.id)
      })
    },
    addNotification(email) {
      api.addNewNotificationChannel(this.monitor.id, email)
      .then(response => {
        this.fetchData(this.monitor.id)
      })
    }
  },
  watch: {
    $route(to, from) {
      //console.log("route change")
      this.fetchData(this.$route.params.id)
      this.$store.dispatch("analysis/fetchAllAnalysis")
    }
  },
  created() {
    this.fetchData(this.$route.params.id)
    this.$store.dispatch("analysis/fetchAllAnalysis")
  },
}

</script>

