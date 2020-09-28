<template>	
<section class='page-container'>
  <div class="columns is-fullheight">
    <div class="is-2 side-menu">
        <div class="field">
  	    <label class="label"> Cliente </label>
  	    <SearchSelect 
  	      :data="clientsSelectOptions"
  	      placeholder="Seleccionar cliente" 
  	      @selected="updateSelectOptions"  
  	      ref=clientselect
  	    />
  	   </div>

    	  <div class="field">
    	    <label class="label"> Contexto </label>
    	    <SearchSelect 
    	      :data="contexts"
    	      placeholder="Seleccionar contexto"
    	      @selected="seriesOptions.contexts = $event"
    	      ref=contextselect
    	    />
    	  </div>

    	  <div class="field">
    	    <label class="label"> Tag </label>
    	    <TreeView :items="tagstree" :displayItems="displayElements" v-model="seriesOptions.tags" />
    	  </div>

        <b-field label="Intervalo agregacion">
          <b-input type="text" :value="seriesOptions.analysisInterval" placeholder="ej: 30m" @input="seriesOptions.analysisInterval = $event" />
        </b-field>

        <b-field class="has-text-right">
          <a class="button is-primary" @click="analize">
            Analizar
          </a>
        </b-field>

    </div>

    <div class="column main-content">
      <TestChart :chartsData="chartsData"/>
      <hr>
    </div>

  </div>  
</section> 
</template>

<script>
import api from "../api/repository";

import TestChart from '../components/TestChart.vue';
import SearchSelect from '../components/SearchSelect.vue';
import TreeView from '../components/TreeView.vue';



export default {
    components: { TestChart, SearchSelect, TreeView },
    data () {
      return {
        seriesOptions: {
          client: '',
          contexts: '',
          tags: [],
          analysisInterval: '1H',
        },

        chartsData: {}
      }
    },
    computed: {     
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
      }
    },
    methods: {
      updateSelectOptions(value) {
          this.seriesOptions.client = value
          this.$store.dispatch('clients/updateTagsContexts', this.seriesOptions.client)
      },
      analize() {
        let payload = { name: this.seriesOptions.client, 
                        tags: this.seriesOptions.tags, 
                        contexts: this.seriesOptions.contexts,
                        interval: this.seriesOptions.analysisInterval}

        if (payload.tags.length == 1 && payload.tags[0] == 'root') {
          payload.tags = []
        }               
        api.testAlgo(payload)
                .then(response => {       
                  this.chartsData = response.data
                })
                .catch(error => { 
                  console.log('error analizing data')
                  console.log(error)
                })
      }
      
    },
}
</script>




<style>
.page-container {
  padding: 1.25rem;
}

.is-fullheight {
  height: calc(100vh - 9rem);
  min-height: calc(100vh - 9rem);
}
  
.side-menu {
  overflow-y: auto;
}

.main-content {
  display: flex;
  flex-direction: column;
  overflow-y: overlay;
  overflow-x: hidden;
}
</style>