<template>

<div>
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
            label="Input must be a number followed by a valid letter [ m = minutes, H = hour, D = day, W = week, M = month, y = year ]"
            size="is-large"
            position="is-bottom"
            multilined>
            <b-input
              v-model="settings.interval"
              type="text"
              size="is-small"              
              validation-message="Invalid format"
              pattern="[0-9]+[mHDWMy]+">
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

export default {
  name: "AnalysisSettings",
  mixins: [tagsAndContexts],
  components:  { SearchSelect, TreeSelect },
  data () {
    return {
      settings: {
        client: '',
        contexts: [],
        tags: [],
        interval: '1H',
        parameters: '',
      }
    }
  },
  computed: {
    clients() {
      return this.$store.getters['clients/readyClients']
    },
  },
  methods: {
    updateSelectOptions(value) {
      this.settings.client = value  
      this.updateContexts(value)
      this.updateTags(value)
    },
    runAnalysis() {
      this.$store.dispatch('analysis/analizeSeries', this.settings)
    }
  }
}
</script>