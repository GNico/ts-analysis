<template>
<div class="container">
  <div class="section">

    <div class="buttons">
      <a class="button is-primary is-small" @click="isModalActive = true"> 
        <b-icon icon="plus" ></b-icon>
        <span>Add client</span>
      </a>
    </div>

    <b-modal :active.sync="isModalActive" has-modal-card>
      <FormNewClient @submit="addClient"/>
    </b-modal>  

    <b-table :data="clients" striped>        
      <template slot-scope="props">
        <b-table-column field="name" label="Client">
          {{ props.row.name }}
        </b-table-column>

        <b-table-column v-if="props.row.indexing" colspan=4 field="count"  label="Status">
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
            {{ formatDate(props.row.created) }}
          </b-table-column>
          <b-table-column field="modified" label="Last modified">
            {{ formatDate(props.row.modified) }}
          </b-table-column>    
          
          <b-table-column label="Action" >
            <b-tooltip label="View details">
              <button class="transparent-button" @click="selectedView = props.row.name">
                <b-icon icon="eye-outline" type="is-primary"></b-icon>
              </button>
            </b-tooltip>
            <b-tooltip label="Edit">
              <button class="transparent-button">
                <b-icon icon="pencil" type="is-primary"></b-icon>
              </button>
            </b-tooltip>
            <b-tooltip label="Settings">
              <button class="transparent-button">
                <b-icon icon="cog" type="is-primary"></b-icon>
              </button>
            </b-tooltip>
            <b-tooltip label="Delete">
              <button class="transparent-button" @click="confirmDelete(props.row.name)">
                <b-icon icon="delete-forever" type="is-primary" size="is-samll"></b-icon>
              </button>
            </b-tooltip>
          </b-table-column> 
        </template>
      </template>      
    </b-table>
  </div>  


  <div class="section">
    <ClientDetails :name="selectedView"/>
  </div>

</div>  
</template>


<script>

import FormNewClient from '../components/FormNewClient'
import ClientDetails from '../components/ClientDetails'

export default {
    components: {  FormNewClient, ClientDetails },
    data() {
      return {
        isModalActive: false,
        polling: null,
        selectedView: null,
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
      },
      confirmDelete(name) {
        this.$buefy.dialog.confirm({
          title: 'Deleting account',
          message: 'Are you sure you want to <b>delete</b> this item? This action cannot be undone.',
          confirmText: 'Delete Account',
          type: 'is-danger',
          hasIcon: true,
          onConfirm: () => this.deleteClient(name) //this.$buefy.toast.open(name)
        })
      },
      deleteClient(name) {
        this.$store.dispatch('clients/deleteClient', name)
      },
      formatDate(input) {
        let dateObj = new Date(input)
        const year = dateObj.getFullYear()
        const month = (dateObj.getMonth()+1).toString().padStart(2, '0')
        const day = dateObj.getDate().toString().padStart(2, '0')
        const hour = dateObj.getHours()
        const minutes = dateObj.getMinutes()
        return `${day}-${month}-${year} ${hour}:${minutes}`
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


<style>
</style>