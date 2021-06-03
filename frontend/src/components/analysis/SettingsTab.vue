<template>
<div class="columns">

  <ModalSaveTemplate
    :isActive="saveTemplateModalActive"
    :allModels="models"
    @close="saveTemplateModalActive = false"
    @update="updateModel"
    @save="saveModel"
  />

  <ModalLoadTemplate
    :isActive="loadTemplateModalActive"
    :allModels="models"
    @close="loadTemplateModalActive = false"
    @load="loadModel"
    @delete="deleteModel"
  />

  <div class="column is-3 pb-0">
    <!--Data options -->
    <div class="subtitle"> Data input </div>
    <b-field horizontal label="Client">
      <SearchSelect
        :value="analysis.client"
        @input="updateAnalysis('client', $event)"
        :data="clients"/>
    </b-field>
    <b-field horizontal label="Tags">
      <TreeSelect 
        class="filters-box"
        rootName="All tags"
        :itemsTree="allTags"
        :value="analysis.tags"
        @input="updateAnalysis('tags', $event)"
    />
    </b-field>
    <b-field horizontal label="Contexts">
      <TreeSelect 
        class="filters-box"
        rootName="All contexts"
        :itemsTree="allContexts"
        :value="analysis.contexts"
        @input="updateAnalysis('contexts', $event)"
    />
    </b-field>
    <b-field horizontal label="Interval">
      <b-input 
        :value="analysis.interval"
        @input="updateAnalysis('interval', $event)"
        type="text" 
        pattern="^[0-9]+[mhd]$" 
        size="is-small" />
    </b-field>       
    <b-field horizontal label="From">
      <b-datepicker          
        :first-day-of-week="1"
        size="is-small"
        :value="analysis.start ? new Date(analysis.start) : null"
        @input="updateAnalysis('start', $event)">
        <button class="button is-primary is-small"
            @click="updateAnalysis('start', new Date())">
            <b-icon icon="calendar-today" size="is-small"></b-icon>
            <span>Today</span>
        </button>

        <button class="button is-danger is-small"
            @click="updateAnalysis('start', null)">
            <b-icon icon="close-thick" size="is-small"></b-icon>
            <span>Clear</span>
        </button>
      </b-datepicker>
    </b-field>
     <b-field horizontal label="To">
      <b-datepicker          
        :first-day-of-week="1"
        size="is-small"
        :value="analysis.end ? new Date(analysis.end) : null"
        @input="updateAnalysis('end', $event)">
        <button class="button is-primary is-small"
            @click="updateAnalysis('end', new Date())">
            <b-icon icon="calendar-today" size="is-small"></b-icon>
            <span>Today</span>
        </button>

        <button class="button is-danger is-small"
            @click="updateAnalysis('end', null)">
            <b-icon icon="close-thick" size="is-small"></b-icon>
            <span>Clear</span>
        </button>
      </b-datepicker>
    </b-field>
    <b-field class="has-text-right sticky-container">
      <div class="box">
        <a class="button is-primary is-medium has-text-weight-semibold" @click="runAnalysis">
          Run analysis
        </a>
      </div>
    </b-field> 
  </div>

  <div class="column is-9 pb-0 right-section">
    <!--Model building -->
    <div class="subtitle is-flex is-justify-content-space-between"> 
      Detection model
      <b-field grouped position="is-right">
        <p class="control">
          <b-button 
            class="has-text-weight-semibold"
            :class="loadTemplateModalActive ? 'is-primary' : 'is-outlined'" 
            label="Import template" 
            size="is-small" 
            type="is-primary" 
            @click="loadTemplateModalActive = !loadTemplateModalActive"/>      
        </p>
        <p class="control">
          <b-button 
            class="has-text-weight-semibold"
            :class="saveTemplateModalActive ? 'is-primary' : 'is-outlined'" 
            label="Save as template" 
            size="is-small" 
            type="is-primary" 
            @click="saveTemplateModalActive = !saveTemplateModalActive"/>      
        </p>
      </b-field>
    </div>
    <ModelBuilder 
      class="pt-2" 
      :nodes="analysis.model"
      @input="updateAnalysis('model', $event)"
    />
  </div>

</div>
</template>


<script>
import TreeSelect from '../inputs/TreeSelect.vue';
import SearchSelect from '../inputs/SearchSelect.vue';
import ModelBuilder from "../detectionModel/ModelBuilder";
import ModalSaveTemplate from "./ModalSaveTemplate"
import ModalLoadTemplate from "./ModalLoadTemplate"

export default {
  components:  { TreeSelect, ModelBuilder, SearchSelect, ModalSaveTemplate, ModalLoadTemplate },
  data () {
    return {
      saveTemplateModalActive: false,  
      loadTemplateModalActive: false,
    }
  },
  computed: {
    clients() {
      return this.$store.getters['clients/readyClients']
    },
    analysis() {
      return this.$store.getters['analysis/activeAnalysis']
    },
    models() {
      return this.$store.state.models.all
    },
    allTags() {
      return this.$store.state.clients.tags[this.analysis.client] 
    },
    allContexts() {
      return this.$store.state.clients.contexts[this.analysis.client] 
    },
  },
  methods: {
    saveModel(modalForm) {
      this.$store.dispatch('models/saveModel', {
        ...modalForm,
        nodes: this.analysis.model
      })
    },
    updateModel(modalForm) {
      this.$store.dispatch('models/updateModel', {
        ...modalForm,
        nodes: this.analysis.model
      })
    },
    loadModel(model) {
      this.updateAnalysis('model', model.nodes)
    },
    deleteModel(id) {
      this.$store.dispatch('models/deleteModel', id)
    },
    runAnalysis() {
      this.$emit('run')
      this.$store.dispatch('analysis/runAnalysis', this.analysis.id)
    },
    updateAnalysis(prop, value) {
      let updatedSettings = {id: this.analysis.id, [prop]: value }
      if (prop == 'client' && value != this.analysis.client) {
        updatedSettings.tags = []
        updatedSettings.contexts = []
      }
      this.$store.dispatch('analysis/updateLocalSettings', updatedSettings)
    }
  },
  watch: {
    'analysis.client': {
      handler(newVal) {
        if (!newVal || this.clients.includes(newVal)) {
          this.$store.dispatch('clients/fetchTags', (newVal))
          this.$store.dispatch('clients/fetchContexts', (newVal))
        }
      }
    },
  },
  created() {
    this.$store.dispatch('models/fetchModels')
  }
}
</script>


<style scoped>
.filters-box {
  padding-top: 0.25rem;
  max-height: 15rem;
  overflow-y: auto;
}

.right-section {
  border-left: 1px solid rgba(255,255,255,0.1);
} 

.sticky-container {
  position: sticky;
  bottom: 0;
}

.sticky-container .box {
  border-radius: 0;
  padding-right: 0;
}


</style>
