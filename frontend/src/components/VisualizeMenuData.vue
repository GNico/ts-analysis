<template>

<div>

  <b-field label="Series name">
    <b-input type="text" size="is-small"/>
  </b-field>

  <b-field label="Client">
    <SearchSelect 
      :saved="saved.client"
      :data="clientsSelectOptions"
      placeholder="Seleccionar cliente" 
      @selected="updateSelectOptions"  
      ref=clientselect
    />
  </b-field>

  <b-field label="Contexts">
    <TreeView :items="contextsTree" :displayItems="displayContexts" v-model="selectedContexts" />

  </b-field>

  <b-field label="Tags">
    <TreeView :items="tagsTree" :displayItems="displayTags" v-model="selectedTags" />
  </b-field>


  <b-field class="has-text-right">
    <a class="button is-primary is-small" @click="analize">
      Apply
    </a>
  </b-field>



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
        return this.$store.state.clients.contexts
    },
    tags() {
        return this.$store.state.clients.tags
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
      async setSavedOptions (value) {
          let obj = this.$store.getters['series/getSeriesOptions'](value) 
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
      }
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