<template>
<div class="card">
  <header class="card-header">
    <p class="card-header-title">
      Add series
    </p>    
  </header>

  <div class="card-content">
    <div class="field is-horizontal">
      <div class="field-label is-normal">
        <label class="label">Name</label>
      </div>
      <div class="field-body">
        <div class="field is-narrow">
          <div class="control">
            <input class="input is-small" type="text" v-model="seriesOptions.name">
          </div>
        </div>
      </div>
    </div>


    <div class="field is-horizontal">
      <div class="field-label is-normal">
        <label class="label">Panel</label>
      </div>
      <div class="field-body">
        <div class="field is-narrow">
          <div class="control">
            <input class="input is-small" type="text" v-model="seriesOptions.yAxis">
          </div>
        </div>
      </div>
    </div>

    <div class="field is-horizontal">
      <div class="field-label is-normal">
        <label class="label">Client</label>
      </div>
      <div class="field-body">
        <div class="field is-narrow">
          <div class="control">
            <SearchSelect 
              :saved="seriesOptions.client"
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
      <div class="field-label is-normal">
        <label class="label">Interval</label>
      </div>
      <div class="field-body">
        <div class="field is-narrow">
          <div class="control">
            <b-tooltip
              label="Input must be a number followed by a valid letter [ m = minutes, H = hour, D = day, W = week, M = month, y = year ]"
              size="is-large"
              position="is-bottom"
              multilined>
              <b-input
                v-model="seriesOptions.interval"
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

  
    <div class="field is-horizontal">
      <div class="field-label is-normal">
        <label class="label">Contexts</label>
      </div>
      <div class="field-body">
        <div class="field is-narrow">
          <div class="control">
            <TreeView 
              class="custom-field"
              :items="contextsTree" 
              :displayItems="displayContexts" 
              v-model="seriesOptions.contexts" 
            />
          </div>
        </div>
      </div>
    </div> 

    <div class="field is-horizontal">
      <div class="field-label is-normal">
        <label class="label">Tags</label>
      </div>
      <div class="field-body">
        <div class="field is-narrow">
          <div class="control">
            <TreeView 
              class="custom-field"
              :items="tagsTree" 
              :displayItems="displayTags" 
              v-model="seriesOptions.tags" 
            />
          </div>
        </div>
      </div>
    </div>

    <div class="field is-grouped is-grouped-right">
      <p class="control">
        <a class="button is-primary is-small" @click="addSeries">
          OK
        </a>
      </p>
      <p class="control">
        <a class="button is-danger is-small" @click="close">
          Cancel
        </a>
      </p>
    </div>

  </div>         
</div>
</template>


<script>

import SearchSelect from './SearchSelect.vue';
import TreeView from './TreeView.vue';
import { tagsAndContexts } from '../mixins/TagsAndContextsOptions.js';

export default {
  name: "VisualizeCardSeries",
  mixins: [tagsAndContexts],
  components: { SearchSelect, TreeView },
  data () {
    return {
      seriesOptions: {
        name: '',
        interval: '1H',
        client: '',
        contexts: [],
        tags: [],
        yAxis: 0,
      },
    }
  },
  computed: {
    clients() {
      return this.$store.getters['clients/readyClients']
    },
  },
  methods: {
    close() {
      this.$emit('close')
    },
    updateSelectOptions(value) {
      this.seriesOptions.client = value  
      this.updateContexts(value)
      this.updateTags(value)
    },
    addSeries() {
      this.$store.dispatch('visualize/addSeries', this.seriesOptions)
      this.close()
    }
  },
  watch: {

  }
}

</script>


<style scoped>



.custom-field {
  margin-top: 0.5rem;
}


</style>