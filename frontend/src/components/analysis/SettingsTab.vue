<template>
<div class="columns">
  <ModalSaveAnalysis 
    :isActive="saveModalActive" 
    @close="saveModalActive = !saveModalActive"
    @update="saveAnalysisOverwrite"
    @save="saveAnalysisAsNew"
  />

  <ModalSaveModel
    :isActive="isSaveModelActive"
    :allModels="models"
    @close="toggleSaveModel"
    @update="updateModel"
    @save="saveModel"
  />

  <div class="column is-3">
    <!--General options -->
    <div class="subtitle subtitle-with-buttons"> 
      General 
      <b-field grouped position="is-right">
        <p class="control">
          <b-button 
            class="is-outlined has-text-weight-semibold" 
            label="Save" 
            size="is-small" 
            type="is-primary" 
            @click="saveAnalysis"/>
        </p>
      </b-field>
    </div>
    <b-field horizontal label="Name">
      <b-input 
        type="text" 
        size="is-small" 
        placeholder="This field is optional"
        v-model="settings.name"/>
    </b-field>
    <b-field horizontal label="Description">
      <b-input 
        type="textarea" 
        size="is-small" 
        placeholder="This field is optional"
        v-model="settings.description"
        />
    </b-field>
    <b-field class="has-text-right">
      <a class="button is-primary is-medium has-text-weight-semibold" @click="runAnalysis">
        Run analysis
      </a>
    </b-field>
    <!--Data options -->
    <div class="subtitle"> Data input </div>
    <b-field horizontal label="Client">
      <SearchSelect
        v-model="settings.client"
        :data="clients"
        @select="clearTagsContexts"/>
    </b-field>
    <b-field horizontal label="Tags">
      <TreeSelect 
        class="filters-box"
        rootName="All tags"
        :itemsTree="allTags"
        v-model="settings.tags"/>
    </b-field>
    <b-field horizontal label="Contexts">
      <TreeSelect 
        class="filters-box"
        rootName="All contexts"
        :itemsTree="allContexts"
        v-model="settings.contexts"/>
    </b-field>
    <b-field horizontal label="Interval">
      <b-input v-model="settings.interval" type="text" pattern="^[0-9]+[mhd]$" size="is-small" />
    </b-field>    
  </div>

  <div class="column is-9 right-section">
    <!--Model building -->
    <div class="subtitle subtitle-with-buttons"> 
      Detection model
      <b-field grouped position="is-right">
        <p class="control">
          <b-dropdown scrollable :max-height="300" aria-role="list" position="is-bottom-left">
            <template #trigger="{ active }">
              <b-button :class="active ? 'is-primary' : 'is-outlined'" label="Import template" size="is-small" type="is-primary" class="has-text-weight-semibold"/>
            </template>
            <b-dropdown-item 
              v-for="item in models" 
              :key="item.id"
              @click="loadModel(item)"
              aria-role="listitem">
              {{item.name}}
            </b-dropdown-item>
          </b-dropdown>
        </p>
        <p class="control">
          <b-button 
            class="has-text-weight-semibold"
            :class="isSaveModelActive ? 'is-primary' : 'is-outlined'" 
            label="Save as template" 
            size="is-small" 
            type="is-primary" 
            @click="toggleSaveModel"/>      
        </p>
      </b-field>
    </div>
    <ModelBuilder class="model-box" :nodes="settings.model"  />
  </div>

</div>
</template>


<script>
import TreeSelect from '../inputs/TreeSelect.vue';
import SearchSelect from '../inputs/SearchSelect.vue';
import ModelBuilder from "../detectionModel/ModelBuilder";
//import ModalCard from "../ModalCard";
import ModalSaveAnalysis from "./ModalSaveAnalysis"
import ModalSaveModel from "./ModalSaveModel"



import { tagsAndContexts } from '../../mixins/TagsAndContextsOptions.js';
import cloneDeep from "lodash/cloneDeep";

const defaultSettings = {
  name: '',
  description: '',
  client: '',
  contexts: [],
  tags: [],
  interval: '1h',
  model: [],
  savedId: '',
}

export default {
  name: "AnalysisSettings",
  mixins: [tagsAndContexts],
  components:  { TreeSelect, ModelBuilder, SearchSelect, ModalSaveAnalysis,ModalSaveModel },
  data () {
    return {
      settings: cloneDeep(defaultSettings),    
      isSaveModelActive: false,  
   /*   modelData: {
        name: '',
        description: '',
      }, */
      saveModalActive: false,
    }
  },
  computed: {
    clients() {
      return this.$store.getters['clients/readyClients']
    },
    id() {
      return this.$store.state.analysis.activeAnalysisId
    },
    models() {
      return this.$store.state.models.all
    },
  },
  methods: {
    toggleSaveModel() {
      this.isSaveModelActive = !this.isSaveModelActive
    },
    saveModel(modalForm) {
      this.isSaveModelActive = false
      this.$store.dispatch('models/saveModel', {
        ...modalForm,
        nodes: this.settings.model
      })
    },
    updateModel(modalForm) {
      this.isSaveModelActive = false
      this.$store.dispatch('models/updateModel', {
        ...modalForm,
        nodes: this.settings.model
      })
    },
    loadModel(model) {
      this.settings.model = cloneDeep(model.nodes)
    },
    resetFields() {
      this.settings = cloneDeep(defaultSettings)
    },
    runAnalysis() {
      this.$emit('run')
      this.$store.dispatch('analysis/runAnalysis', this.id)
    },
    clearTagsContexts(selectevent) {
      if (selectevent) {
        this.settings.tags = []
        this.settings.contexts = []
      }
    },
    saveAnalysis() {
      if (this.settings.savedId) {
        this.saveModalActive = true
      } else {
        this.saveAnalysisAsNew()
      }        
    },
    saveAnalysisAsNew() {
      this.$store.dispatch('analysis/saveAnalysis', this.id)
      .then(savedId => {
        console.log(savedId)
        this.settings.savedId = savedId
      })
    },
    saveAnalysisOverwrite() {
      this.$store.dispatch('analysis/updateAnalysis', this.id)     
    },
  },
  watch: {
    settings: {
      deep: true,
      handler(newVal) {
        this.$store.dispatch('analysis/updateLocalSettings', {id: this.id, ...this.settings })
      }
    },
    'settings.client': {
      handler(newVal) {
        if (!newVal || this.clients.includes(newVal)) {
          this.updateTags(newVal)
          this.updateContexts(newVal)  
        }
      }
    },
    id: {
      immediate: true,
      handler(newVal) {
        const storeSettings = this.$store.getters['analysis/getAnalysisById'](newVal) 
        this.resetFields()
        for (const key of Object.keys(storeSettings)) {
          if (this.settings.hasOwnProperty(key)) { 
            this.settings[key] = storeSettings[key]
          }
        }        
      }
    }
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

</style>
