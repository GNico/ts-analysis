<template>
  
<div class="modal-card">
  <header class="modal-card-head">
    <p class="modal-card-title">Series</p>
  </header>

  <section class="modal-card-body">
    <div class="field">
      <label class="label"> Nombre </label>
      <b-field v-if="edit">
        <b-select placeholder=""  :value="seriesOptions.name" @input="setSavedOptions"> 
          <option v-for="item in seriesNames"> {{ item }}</option>
        </b-select>     
        <p class="control">
          <button class="button is-primary" @click="createMode">
            <span class="icon">
              <i class="fas fa-plus"></i>
            </span>
          </button>
        </p>
      </b-field>
      <div v-else>
        <b-field> 
          <b-input v-model="seriesOptions.name" ></b-input>
          <p class="control">
            <button class="button is-danger" @click="editMode">
              <span class="icon">
                <i class="fas fa-times"></i>
              </span>
            </button>
          </p>
        </b-field>
        <p v-show="hasError" class="help is-danger">El nombre ya existe</p>
      </div>
    </div>

  <div class="field">
    <label class="label"> Cliente </label>
    <SearchSelect 
      :saved="saved.client"
      :data="clientsSelectOptions"
      placeholder="Seleccionar cliente" 
      @selected="updateSelectOptions"  
      ref=clientselect
    />
  </div>

  <div class="field">
    <label class="label"> Contexto </label>
    <SearchSelect 
      :saved="saved.contexts" 
      :data="contexts"
      placeholder="Seleccionar contexto"
      @selected="seriesOptions.contexts = $event"
      ref=contextselect
    />
  </div>

  <div class="field">
    <label class="label"> Tag </label>
    <TreeView :items="tagstree" :displayItems="displayElements" v-model="selectedTags" />
  </div>
  </section>

  <footer class="modal-card-foot">
    <div v-if="edit" class="buttons is-centered ">
      <a class="button is-primary" @click="updateSeries">
        Actualizar
      </a>
      <a class="button is-danger" @click="deleteSeries">
        Eliminar
      </a>
    </div>
    <div v-else class="buttons is-centered">
      <a class="button is-primary" @click="addSeries">
        Agregar
      </a>
      <a class="button is-danger" @click="editMode">
        Cancelar
      </a>
    </div>    
  </footer>

</div>
</template>


<script>
import SearchSelect from './SearchSelect.vue';
import TreeView from './TreeView.vue';


/*<SearchSelect 
      :saved="saved.tags" 
      :data="tags"
      placeholder="Seleccionar tag"
      @selected="seriesOptions.tags = $event"
      ref=tagselect
    />*/


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
    tagstree() {
      let tree =  { name: 'All tags', id: "root", children: this.tags.tree }
      return tree
    },
    displayElements() {
      return { name: this.tagstree.name,
               id: this.tagstree.id,
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


<style>
  
.menu-overlap {
  position:static;
  top:0;

  z-index:99; 

}  
</style>