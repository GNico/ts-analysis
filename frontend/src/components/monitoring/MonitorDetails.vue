<template>
<div class="p-5"> 
  <ModalLoadAnalysis 
    :allAnalysis="savedAnalysis"
    :isActive="loadModalActive" 
    @close="loadModalActive = false"
    @load="addItem"
    title="Select Analysis"
    :allowDelete="false"
    confirmLabel="Create Detector"
  />
  
  <ModalDetectorGraph
    :model="modelData"
    :isActive="modelModalActive"
    @close="modelModalActive = false"
  />

  <div class="title">{{ monitor.name }}</div>
  <b-tabs type="is-medium"  :animated="false"  destroy-on-hide>
    <b-tab-item label="Detectors" icon="alarm-light" value="Detectors">
      <div class="is-flex is-justify-content-space-between">
        <b-input placeholder="Search"> </b-input>
        <a class="button is-primary" @click="loadModalActive = !loadModalActive">
          <b-icon icon="playlist-plus"></b-icon>
          <span class="has-text-weight-semibold">Add detector</span>
        </a>
      </div>
      

      <CardDetector 
        v-for="detector in monitor.detectors" 
        :key="detector.id"
        :detector="detector"
        @delete="deleteItem"
        @update="updateOpts"
        @editAnalysis="editAnalysis"
        @showGraph="showGraph"
        />

    </b-tab-item>

    <b-tab-item label="Notification channels" icon="bell" value="Notifications">

      
      <span class="is-size-5"> {{monitor.notification_email}} </span>
    </b-tab-item>
    
  </b-tabs>

  


</div>
</template>

<script>
import api from '@/api/repository'
import ModalLoadAnalysis from '@/components/analysis/ModalLoadAnalysis'
import ModalDetectorGraph from './ModalDetectorGraph'
import CardDetector from './CardDetector'

export default {
  components: { ModalDetectorGraph, ModalLoadAnalysis, CardDetector },
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

      modelModalActive: false,
      modelData: [],
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
      api.getMonitorDetails(monitorId)
      .then(response => {
        this.monitor = { ...response.data }
      })
    },
    addItem(id) {
      api.addNewPeriodicAnalysis(this.monitor.id, id)
      .then(response => {
        this.fetchData(this.monitor.id)
        this.$buefy.toast.open({
          message: "Detector created",
          type: 'is-success',
          duration: 2500,
        })
      })
      .catch(error => console.log(error))
    },
    deleteItem(id) {
      api.deletePeriodicAnalysis(this.monitor.id, id)
      .then(response => {
        this.fetchData(this.monitor.id)
      })
    },
    updateOpts(options) {
      this.$emit('update', options)
    },
    editAnalysis(analysis) {
      //should switch to analysis page
      console.log(analysis)
    },
    showGraph(data) {
      this.modelModalActive = true
      this.modelData = data
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

