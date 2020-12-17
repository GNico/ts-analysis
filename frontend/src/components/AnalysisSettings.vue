<template>
<div>
  <b-field horizontal label="Name">
    <b-input 
          type="text" 
          size="is-small" 
          placeholder="This field is optional"
          v-model="settings.name"/>
  </b-field>

  <b-field horizontal label="Client">
    <SearchSelect 
          :saved="settings.client"
          :data="clients"
          @selected="updateSelectOptions"
          size="is-small"
          placeholder="" 
          ref=clientselect />
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

  <b-field horizontal label="Parameters">
       <b-input type="textarea" 
             v-model="settings.parameters"
             placeholder="ej: {parametername: value, parametername2: value2}"/>
  </b-field>

  <b-field class="has-text-right">
    <a class="button is-primary" @click="runAnalysis">
      Run analysis
    </a>
  </b-field>
</div>
</template>


<script>
import SearchSelect from './SearchSelect.vue';
import TreeSelect from './TreeSelect.vue';
import { tagsAndContexts } from '../mixins/TagsAndContextsOptions.js';

const defaultSettings = {
  name: '',
  client: '',
  contexts: [],
  tags: [],
  interval: '1h',
  parameters: '',
}

export default {
  name: "AnalysisSettings",
  mixins: [tagsAndContexts],
  components:  { SearchSelect, TreeSelect },
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
    updateSelectOptions(value) {
      this.settings.client = value  
      this.updateContexts(value)
      this.updateTags(value)
    },
    resetFields() {
      this.settings = { ...defaultSettings }
    },
    runAnalysis() {
      this.$emit('run')
      this.$store.dispatch('analysis/runAnalysis', this.id)
    }
  },
  watch: {
    settings: {
      deep: true,
      handler(newVal) {
        this.$store.dispatch('analysis/updateSettings', {id: this.id, ...this.settings})
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