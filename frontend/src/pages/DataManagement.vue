<template>
<div class="container">
  <div class="section">
    <b-dropdown ref="dropdown" class="mb-3" position="is-bottom-right" append-to-body trap-focus>
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
      :default-sort="['name', 'asc']"
      detailed    
      :opened-detailed="openRows"
      detail-key="name"
      :show-detail-icon="false"
      striped>       
      <b-table-column sortable field="name" label="Client" v-slot="props">
        {{ props.row.name }}
      </b-table-column>

      <b-table-column 
        sortable 
        field="count" 
        label="Status" 
        v-slot="props"
        :td-attrs="(row) => ({colspan: getRowProps(row).colspan})">
        <span v-if="getRowProps(props.row).colspan == 1" class="tag" :class="getRowProps(props.row).classColor">
          {{props.row.status}}
        </span> 
        <div v-else class="columns is-vcentered">
          <div class="column is-3">
            <span class="tag" :class="getRowProps(props.row).classColor">
              {{ props.row.status }}
            </span> 
          </div>
          <div class="column">
            <b-progress type="is-info" size="is-large" :value="props.row.progress" show-value format="percent"></b-progress>
          </div>
        </div>
      </b-table-column>

      <b-table-column 
        sortable field="created"  
        label="Created" 
        v-slot="props"
        :td-attrs="(row) => ({class: getRowProps(row).colspan == 1 ? '' : 'is-hidden'})">
        {{ formatDate(props.row.created) }}
      </b-table-column>

      <b-table-column 
        sortable field="modified" 
        label="Last modified" 
        v-slot="props"
        :td-attrs="(row) => ({class: getRowProps(row).colspan == 1 ? '' : 'is-hidden'})">
        {{ formatDate(props.row.modified) }}
      </b-table-column>    

      <b-table-column 
        label="Action" 
        v-slot="props"
        :td-attrs="(row) => ({class: getRowProps(row).colspan == 1 ? '' : 'is-hidden'})">
        <template v-if="props.row.status == 'Ready'">
          <b-tooltip label="View details">
            <button class="transparent-button" @click="toggleDetails(props.row.name)">
              <b-icon icon="eye-outline" type="is-primary"></b-icon>
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

      <!--Row details-->
      <template #detail="props">
        <ClientDetails :name="props.row.name" :clientDetails="clientDetails"/>
      </template>  
    </b-table>
  </div>  
</div>  
</template>


<script>
import FormNewClient from '@/components/dataManagement/FormNewClient'
import ClientDetails from '@/components/dataManagement/ClientDetails'
import api from '@/api/repository'
import { formatDate } from '@/utils/dateFormatter'

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
      getRowProps(row) {
        switch (row.status) {
          case 'Ready': 
            return {
              classColor: 'is-success',
              colspan: 1,
            }
          case 'Failed': 
            return {
              classColor: 'is-danger',
              colspan: 1,
            }
          case 'Indexing': 
            return {
              classColor: 'is-info',
              colspan: 4,
            }
          case 'Waiting': 
            return {
              classColor: 'is-link',
              colspan: 4,
            }
        }
      }
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