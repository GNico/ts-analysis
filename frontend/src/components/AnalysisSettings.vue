<template>

<div>
  <div class="field is-horizontal">
    <div class="field-label has-text-left">
      <label class="label">Name</label>
    </div>
    <div class="field-body">
      <div class="field is-narrow short-field">
        <div class="control">
          <b-input 
            type="text" 
            size="is-small" 
            placeholder="This field is optional"
            v-model="settings.name"/>
        </div>
      </div>
    </div>
  </div>

  <div class="field is-horizontal">
    <div class="field-label has-text-left">
      <label class="label">Client</label>
    </div>
    <div class="field-body">
      <div class="field is-narrow short-field">
        <div class="control">
          <SearchSelect 
            :saved="settings.client"
            :data="clients"
            @selected="updateSelectOptions"
            size="is-small"
            placeholder="" 
            ref=clientselect
          />
        </div>
      </div>
    </div>
  </div>

  <b-field class="field is-horizontal">
    <div class="field-label has-text-left">
      <label class="label">Tags</label>
    </div>
    <div class="field-body">
      <TreeSelect 
        class="filters-box"
        rootName="All tags"
        :itemsTree="allTags"
        v-model="settings.tags" 
      />
    </div>
  </b-field>

  <b-field class="field is-horizontal">
    <div class="field-label has-text-left">
      <label class="label">Contexts</label>
    </div>
    <div class="field-body">
      <TreeSelect 
        class="filters-box"
        rootName="All contexts"
        :itemsTree="allContexts"
        v-model="settings.contexts" 
      />
    </div>
  </b-field>
  
  <b-field class="field is-horizontal">
    <div class="field-label has-text-left">
      <label class="label">Interval</label>
    </div>
    <div class="field-body">
      <div class="field is-narrow shorter-field">
        <div class="control">
          <b-tooltip
            label="Input must be a number followed by a valid letter [ m = minutes, h = hour, d = day ]"
            size="is-large"
            position="is-bottom"
            multilined>
            <b-input
              v-model="settings.interval"
              type="text"
              size="is-small"              
              validation-message=""
              pattern="[0-9]+[mhd]+">
            </b-input> 
          </b-tooltip>          
        </div>              
      </div>
    </div>
  </b-field>

  <b-field label="Parameters">
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