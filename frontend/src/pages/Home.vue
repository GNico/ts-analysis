<template>
<div class="container">
  <div class="section">
    <b-dropdown ref="dropdown" class="top-button" position="is-bottom-right" append-to-body trap-focus>
      <a
        class="button is-primary is-small"
        slot="trigger"
        role="button">
        <b-icon  icon="playlist-plus"></b-icon>
        <span class="has-text-weight-semibold">New Entry</span>
      </a>
      <b-dropdown-item
        aria-role="menu-item"
        :focusable="false"
        custom
        paddingless>
        <FormNewClient :dataSourceNames="dataSourceNames" @submit="addClient"/>
      </b-dropdown-item>
    </b-dropdown>

    <b-table 
      :data="clients" 
      detailed    
      :opened-detailed="openRows"
      detail-key="name"
      :show-detail-icon="false"
      striped>       

      <template slot-scope="props">
        <b-table-column sortable field="name" label="Client">
          {{ props.row.name }}
        </b-table-column>

        <!--Ready status-->
        <template v-if="['Ready','Failed'].includes(props.row.status)")>
          <b-table-column sortable field="count" label="Status">
            <span class="tag" :class="props.row.status == 'Ready' ? 'is-success' : 'is-danger'">
              {{props.row.status}}
            </span> 
          </b-table-column>
          <b-table-column sortable field="created"  label="Created">
            {{ formatDate(props.row.created) }}
          </b-table-column>
          <b-table-column sortable field="modified" label="Last modified">
            {{ formatDate(props.row.modified) }}
          </b-table-column>    
          
          <b-table-column label="Action" >
            <template v-if="props.row.status == 'Ready'">
              <b-tooltip label="View details">
                <button class="transparent-button" @click="toggleDetails(props.row.name)">
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
            </template>
            <b-tooltip label="Delete">
              <button class="transparent-button" @click="confirmDelete(props.row.name)">
                <b-icon icon="delete-forever" type="is-primary" size="is-samll"></b-icon>
              </button>
            </b-tooltip>
          </b-table-column> 
        </template>

        <!--Other status-->
        <b-table-column v-else colspan=4 sortable field="count"  label="Status">
          <div class="columns is-vcentered">
            <div class="column is-3">
              <span class="tag" :class="props.row.status == 'Indexing' ? 'is-info' : 'is-link'">
                {{ props.row.status }}
              </span> 
            </div>
            <div class="column">
              <b-progress type="is-info" size="is-large" :value="props.row.progress" show-value format="percent"></b-progress>
            </div>
          </div>
        </b-table-column>

      </template>    

      <!--Row details-->
      <template slot="detail" slot-scope="props">
        <ClientDetails :name="props.row.name" :clientDetails="clientDetails"/>
      </template>  
    </b-table>
  </div>  
</div>  
</template>


<script>
import FormNewClient from '../components/FormNewClient'
import ClientDetails from '../components/ClientDetails'
import api from '../api/repository'
import { formatDate } from '../utils/helpers'


export default {
    components: {  FormNewClient, ClientDetails },
    data() {
      return {
        polling: null,
        openRows: [],
        dataSourceNames: []
      }
    },
    computed: {
      clients() {        
        return this.$store.state.clients.clients
      },
      clientDetails() {
        return this.$store.state.clients.details
      }
    },
    methods: {
      pollClients () {
        this.polling = setInterval(() => {
          this.$store.dispatch('clients/fetchClients')          
        }, 3000)
      },
      addClient(form) {
        this.$store.dispatch('clients/addClient', form)
        this.$refs.dropdown.isActive = false
        this.$buefy.toast.open({
          message: 'Creating new entry',
          type: 'is-success',
          duration: 2500,
        })
      },      
      confirmDelete(name) {
        this.$buefy.dialog.confirm({
          title: 'Deleting client',
          message: 'Are you sure you want to <b>delete</b> this item? This action cannot be undone.',
          confirmText: 'Delete Client',
          type: 'is-danger',
          scroll: 'keep',
          hasIcon: true,
          onConfirm: () => this.deleteClient(name)
        })
      },
      deleteClient(name) {
        this.$store.dispatch('clients/deleteClient', name)
        this.$buefy.toast.open({
          message: 'Deleting ' + name,
          type: 'is-danger',
        })
      },
      formatDate(input) {
        return formatDate(input)
      },    
      toggleDetails(name) {
        let index = this.openRows.findIndex(elem => elem == name)
        if (index != -1) {
          this.openRows.splice(index, 1)
        } else {
          this.openRows.push(name)
          this.$store.dispatch('clients/fetchClientDetails', name) 
        }
      },
    },
    created () {
      this.pollClients()
      api.getDataSourceNames().then(response => this.dataSourceNames = response.data)
    },
    beforeDestroy () {
      clearInterval(this.polling)
    },
}
</script>


<style scoped>
.top-button {
  margin-bottom: 0.75rem;
}
</style>