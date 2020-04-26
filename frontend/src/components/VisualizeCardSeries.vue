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
            <input class="input is-small" type="text">
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
              :saved="saved.client"
              size="is-small"
              :data="clientsSelectOptions"
              placeholder="Seleccionar cliente" 
              @selected="updateSelectOptions"  
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
              v-model="selectedContexts" 
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
              v-model="selectedTags" 
            />
          </div>
        </div>
      </div>
    </div>

    <div class="field is-grouped is-grouped-right">
      <p class="control">
        <a class="button is-primary is-small">
          OK
        </a>
      </p>
      <p class="control">
        <a class="button is-danger is-small" @click="$emit('close')">
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

export default {
  components: { SearchSelect, TreeView },
  data () {
    return {
      seriesOptions: {
        name: '',
        client: '',
        contexts: '',
        tags: '',
      },
      saved: {
        client: '',
        contexts: '',
        tags: '',
      },
      edit: false, 
      isOpen: false,
      selectedTags: [],
    }
  },
  computed: {
    seriesNames() {
        return this.$store.getters['series/getSeriesNames']
    },
    clients() {
        return this.$store.state.clients.clients
    },
    clientsSelectOptions() {
        return this.clients.map(item => item.name);
    },
    contexts() {
        //return this.$store.state.clients.contexts
        return []
    },
    tags() {
        return []
        //return this.$store.state.clients.tags
    },
    tagsTree() {
      let tree =  { name: 'All tags', id: "root", children: this.tags.tree }
      return tree
    },
    contextsTree() {
      let tree =  { name: 'All contexts', id: "root", children: this.contexts.tree }
      return tree
    },
    displayTags() {
      return { name: this.tagsTree.name,
               id: this.tagsTree.id,
               children: [] }
    },
    displayContexts() {
      return { name: this.contextsTree.name,
               id: this.contextsTree.id,
               children: [] }
    },
    hasError() {
        return this.seriesNames.includes(this.seriesOptions.name)
    }
  },
  methods: {
/*          let obj = this.$store.getters['series/getSeriesOptions'](value) 
          this.seriesOptions.name = value
          this.saved.client = obj.client 
          await this.$store.dispatch('clients/updateTagsContexts', obj.client)
          this.saved.tags = obj.tags
          this.saved.contexts = obj.contexts
      },
      updateSelectOptions(value) {
          this.seriesOptions.client = value
          if (this.saved.client != value) {
              this.$store.dispatch('clients/updateTagsContexts', this.seriesOptions.client)
          }
      },
      addSeries() {
          this.edit = true
          this.$store.dispatch('series/addSeries', this.seriesOptions)
      },
      updateSeries() {
          this.$store.dispatch('series/updateSeries', this.seriesOptions)
      },
      deleteSeries() {
          this.$store.dispatch('series/deleteSeries', this.seriesOptions.name)
      },
      clearFields() {
          this.seriesOptions.name = ''
          this.$refs.clientselect.clear()
          this.$refs.contextselect.clear()
          this.$refs.tagselect.clear()
          this.saved.client = ''
          this.saved.contexts = ''
          this.saved.tags = ''
      },
      editMode() {
          this.edit = true
      },
      createMode() {
          this.edit = false
          this.clearFields()
      }, */
  },
  watch: {
      seriesNames() {
          if (!this.seriesNames.includes(this.seriesOptions.name) && this.edit) {
              this.clearFields()
          } 
      }
  }
}

</script>


<style scoped>

.card {
  min-width: 500px;
}

.custom-field {
  margin-top: 0.5rem;
}


</style>