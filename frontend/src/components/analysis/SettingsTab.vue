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
    <div class="subtitle"> Data source </div>  
    <div class="inputs-box p-3 has-background-grey-dark">
      <div class="is-flex is-justify-content-space-between mb-4">
        <span class="is-size-5 has-text-white"> Input definition </span>
        <b-button
          class="is-outlined"
          label="Add Input" 
          type="is-info"
          size="is-small"
          @click="addInput"/>        
      </div>

      <InputCard v-for="(input, index) in analysis.data_options"
        :index="index"
        :key="index"
        :client="analysis.client"
        :dataOptions="input"
        :allClients="clients"
        :tagOptions="allTags"
        :contextOptions="allContexts"
        @update="updateAnalysis"
        @delete="deleteInput"/>
    </div>

    <b-field class="has-text-right sticky-container">
      <div class="box">
        <a class="button is-primary is-medium has-text-weight-semibold" @click="runAnalysis">
          Run analysis
        </a>
      </div>
    </b-field> 
  </div>

  <div class="column pb-0 right-section">
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
      class="pt-1" 
      :nodes="analysis.model"
      @input="updateAnalysis({prop: 'model', value: $event})"
    />
  </div>

</div>
</template>


<script>
import ModelBuilder from "../detectionModel/ModelBuilder";
import ModalSaveTemplate from "./ModalSaveTemplate";
import ModalLoadTemplate from "./ModalLoadTemplate";
import InputCard from "@/components/analysis/InputCard";
import cloneDeep from "lodash/cloneDeep";

export default {
  components:  { ModelBuilder, ModalSaveTemplate, ModalLoadTemplate, InputCard },
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
    updateAnalysis({prop, value, index}) {
      let updatedSettings = undefined
      if (prop === 'client' || prop === 'model') {
        updatedSettings = {id: this.analysis.id, [prop]: value }
        // reset tag and contexts if client changed
        if (prop == 'client' && value !=  this.analysis.client) {
          let dataOptionsCopy = cloneDeep(this.analysis.data_options)
          dataOptionsCopy.forEach(elem => {
            elem.tags = []
            elem.contexts = []
          })    
          updatedSettings.data_options = dataOptionsCopy  
        }
      } else {
        let dataOptionsCopy = cloneDeep(this.analysis.data_options)
        dataOptionsCopy[index][prop] = value
        updatedSettings = { id: this.analysis.id, data_options: dataOptionsCopy}
      }
      this.$store.dispatch('analysis/updateLocalSettings', updatedSettings)
    },
    addInput() {
      let dataOptionsCopy = cloneDeep(this.analysis.data_options)
      dataOptionsCopy.push({
        filterContexts: false,
        contexts: [],
        filterTags: false,
        tags: [],
        interval: '1h',
        start: null,
        end: null,
      })
      this.$store.dispatch('analysis/updateLocalSettings', {id: this.analysis.id, data_options: dataOptionsCopy})      
    },
    deleteInput(index) {
      let dataOptionsCopy = cloneDeep(this.analysis.data_options)
      dataOptionsCopy.splice(index, 1)
      this.$store.dispatch('analysis/updateLocalSettings', {id: this.analysis.id, data_options: dataOptionsCopy})      
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
  border-left: 2px solid #073642;
} 

.sticky-container {
  position: sticky;
  bottom: 0;
}

.sticky-container .box {
  border-radius: 0;
  padding-right: 0;
}

.inputs-box {
  margin-right: 0;
  margin-left: 0;
  border: 2px solid rgba(255,255,255,0.1);
}
</style>
