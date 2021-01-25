<template>
<div class="columns">
  <div class="column is-3">
    <!--General options -->
    <div class="subtitle subtitle-with-buttons"> 
      General 
      <b-field grouped position="is-right">
        <p class="control">
          <b-button class="is-outlined" label="Load" size="is-small" type="is-primary" />
        </p>
        <p class="control">
          <b-button class="is-outlined"  label="Save" size="is-small"  type="is-primary" />
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
        />
    </b-field>
    <b-field class="has-text-right">
      <a class="button is-primary is-medium" @click="runAnalysis">
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
          <b-button class="is-outlined" label="Load model" size="is-small" type="is-primary" />
        </p>
        <p class="control">
          <b-button class="is-outlined"  label="Save model" size="is-small"  type="is-primary" />
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
import { tagsAndContexts } from '../../mixins/TagsAndContextsOptions.js';
import cloneDeep from "lodash/cloneDeep";

const defaultSettings = {
  name: '',
  client: '',
  contexts: [],
  tags: [],
  interval: '1h',
  model: []
}

export default {
  name: "AnalysisSettings",
  mixins: [tagsAndContexts],
  components:  { TreeSelect, ModelBuilder, SearchSelect },
  data () {
    return {
      settings: cloneDeep(defaultSettings)
    }
  },
  computed: {
    clients() {
      return this.$store.getters['clients/readyClients']
    },
    id() {
      return this.$store.state.analysis.activeAnalysisId
    }
  },
  methods: {
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
    }
  },
  watch: {
    settings: {
      deep: true,
      handler(newVal) {
        this.$store.dispatch('analysis/updateSettings', {id: this.id, ...this.settings })
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
