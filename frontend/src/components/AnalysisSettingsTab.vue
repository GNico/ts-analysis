<template>
<div class="columns">
  <!--Data options -->
  <div class="column is-3">
    <b-field horizontal label="Name">
      <b-input 
        type="text" 
        size="is-small" 
        placeholder="This field is optional"
        v-model="settings.name"/>
    </b-field>
    <b-field horizontal label="Client">
      <b-autocomplete
        v-model="settings.client"
        open-on-focus
        :data="clients"
        size="is-small"
        ref=autocomplete 
        @select="clearTagsContexts"
        @keydown.native.enter="$event.target.blur()"> 
          <template slot="empty">No results</template>
      </b-autocomplete>  
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

    <b-field class="has-text-right">
      <a class="button is-primary" @click="runAnalysis">
        Run analysis
      </a>
    </b-field>
  </div>

  <!--Model building -->
  <div class="column is-9 right-section">
    <ModelBuilder :model="settings.model" @modelChange="settings.model = $event" />
  </div>
</div>
</template>


<script>
import TreeSelect from './inputs/TreeSelect.vue';
import ModelBuilder from "./detectionModel/ModelBuilder";
import { tagsAndContexts } from '../mixins/TagsAndContextsOptions.js';

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
  components:  { TreeSelect, ModelBuilder },
  data () {
    return {
      settings: { ...defaultSettings }
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
      this.settings = { ...defaultSettings }
    },
    runAnalysis() {
      this.$emit('run')
      this.$store.dispatch('analysis/runAnalysis', this.id)
    },
    clearTagsContexts(selectevent) {
      if (selectevent[0]) {
        this.settings.tags = []
        this.settings.contexts = []
      }
    }
  },
  watch: {
    settings: {
      deep: true,
      handler(newVal) {
        this.$store.dispatch('analysis/updateSettings', {id: this.id, ...this.settings})
      }
    },
    'settings.client': {
      handler(newVal, oldVal) {
        this.updateTags(newVal)
        this.updateContexts(newVal)      
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


<style>
.filters-box {
  padding-top: 0.25rem;
  max-height: 15rem;
  overflow-y: auto;
}
</style>
