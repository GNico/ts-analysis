<template>
    
<div class="container">
  <div class="section">

    <a class="button  is-primary" @click="isModalActive = true"> 
      New entry
    </a>

    <b-table 
      :data="clients" 
      detailed 
      striped        
      bordered >  

      <template slot-scope="props">
        <b-table-column field="name" label="Cliente">
            {{ props.row.name }}
        </b-table-column>

        <b-table-column v-if="props.row.indexing" colspan=3 field="count"  label="Status">
            <div class="columns is-vcentered">
              <div class="column is-3">
                <span class="tag is-info">
                  Indexing...
                </span> 
              </div>
              <div class="column">
                <b-progress type="is-info" size="is-large" :value="props.row.progress" show-value format="percent"></b-progress>
              </div>
            </div>
        </b-table-column>

        <template v-else>
            <b-table-column field="count" label="Status">
              <span class="tag is-success">
                Ready
              </span> 
            </b-table-column>
            <b-table-column field="created"  label="Created">
              {{ props.row.created }}
            </b-table-column>
            <b-table-column field="modified" label="Last modified" >
              {{ props.row.modified }}
            </b-table-column>    
        </template>
      </template>

      <template slot="detail" slot-scope="props">
        <article class="media">
          <figure class="media-left">
            <p class="image is-64x64">
            </p>
          </figure>
          <div class="media-content">
            <div class="content">
              <p>
                Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                Proin ornare magna eros, eu pellentesque tortor vestibulum ut.
                Maecenas non massa sem. Etiam finibus odio quis feugiat facilisis.
              </p>
            </div>
          </div>
        </article>
      </template>
    </b-table>
        
    <b-modal :active.sync="isModalActive" has-modal-card>
      <FormNewClient @submit="addClient"/>
    </b-modal>  

  </div>  
</div>  
</template>


<script>

import FormNewClient from '../components/FormNewClient'

export default {
    components: {  FormNewClient },
    data() {
      return {
        isModalActive: false,
        selected: null,
        polling: null,
      }
    },
    computed: {
      clients() {        
        return this.$store.state.clients.clients
      },
    },
    methods: {
      pollClients () {
        this.polling = setInterval(() => {
          this.$store.dispatch('clients/fetchClients')          
        }, 3000)
      },
      addClient(form) {
        this.isModalActive = false
        this.$store.dispatch('clients/addClient', form)
      }
    },
    created () {
      this.pollClients()
    },
    beforeDestroy () {
      clearInterval(this.polling)
    },
}

</script>