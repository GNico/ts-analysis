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

  <div class="column is-3">
    <!--Data options -->
    <div class="subtitle"> Data input </div>
    <b-field horizontal label="Client">
      <SearchSelect
        :value="analysis.client"
        @input="updateAnalysis('client', $event)"
        :data="clients"
        @select="clearTagsContexts"/>
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
    <b-field class="has-text-right sticky-container">
      <div class="box has-background-grey-darker">
        <a class="button is-primary is-medium has-text-weight-semibold" @click="runAnalysis">
          Run analysis
        </a>
      </div>
    </b-field> 
  </div>

  <div class="column is-9 right-section">
    <!--Model building -->
    <div class="subtitle subtitle-with-buttons"> 
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
    <ModelBuilder class="model-box" :nodes="analysis.model" @input="updateAnalysis('model', $event)" />
  </div>

</div>
</template>


<script>
import TreeSelect from '../inputs/TreeSelect.vue';
import SearchSelect from '../inputs/SearchSelect.vue';
import ModelBuilder from "../detectionModel/ModelBuilder";

import ModalSaveTemplate from "./ModalSaveTemplate"
import ModalLoadTemplate from "./ModalLoadTemplate"

import { tagsAndContexts } from '../../mixins/TagsAndContextsOptions.js';
import cloneDeep from "lodash/cloneDeep";
import isEmpty from "lodash/isEmpty";



export default {
  name: "AnalysisSettings",
  mixins: [tagsAndContexts],
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
  },
  methods: {
    saveModel(modalForm) {
      this.$store.dispatch('models/saveModel', {
        ...modalForm,
      //  nodes: this.settings.model
      })
    },
    updateModel(modalForm) {
      this.$store.dispatch('models/updateModel', {
        ...modalForm,
    //    nodes: this.settings.model
      })
    },
    loadModel(model) {
    //  this.settings.model = cloneDeep(model.nodes)
    },
    deleteModel(id) {
      this.$store.dispatch('models/deleteModel', id)
    },
    resetFields() {
  //    this.settings = cloneDeep(defaultSettings)
    },
    runAnalysis() {
      this.$emit('run')
      this.$store.dispatch('analysis/runAnalysis', this.analysis.id)
    },
    clearTagsContexts(selectevent) {
      if (selectevent) {
    //    this.settings.tags = []
    //    this.settings.contexts = []
      }
    },
    updateAnalysis(prop, value) {
      console.log("updating prop settings")
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
          this.updateTags(newVal)
          this.updateContexts(newVal)  
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

.subtitle-with-buttons {
  display: flex;
  justify-content: space-between;
}

.right-section {
  border-left: 1px solid rgba(255,255,255,0.1);
} 

.model-box {
  padding-top: 0.5rem;
}

.sticky-container {
  position: sticky;
  bottom: 0;
}

.sticky-container .box {
  border-radius: 0;
  padding-right: 0;
}

.column {
  padding-bottom: 0;
}

</style>
