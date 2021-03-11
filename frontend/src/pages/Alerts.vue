<template>
<div class="container section"> 

  <b-table 
    :data="allAnalysis" 
    sticky-header
    checkbox-position="right"
    checkable
    selectable
    :checked-rows.sync="checked">
    <template slot-scope="props">  

      <b-table-column field="client" label="Client" sortable  >
        {{ props.row.client }}       
      </b-table-column>

      <b-table-column field="name" label="Name" sortable >
        {{ props.row.name }}      
      </b-table-column>

      

      <b-table-column field="description" label="Description" >
        {{ props.row.description }}       
      </b-table-column>

      <b-table-column field="monitoring" label="Monitoring">
        <span class="tag is-warning"">
          Offline
        </span>
      </b-table-column>

      <b-table-column field="alerts" label="Alerts">
        <span class="tag is-warning"">
          Disabled
        </span>
      </b-table-column>


      <b-table-column field="load" label="Load">
        <button class="transparent-button" @click="load(props.row.id)">
          <b-icon icon="folder-download" type="is-primary"></b-icon>
        </button>
      </b-table-column>
    </template>
  </b-table>


  
    <button class="button is-small is-danger" :disabled="!checked.length" @click="deleteSelected">Delete selected</button>
    <button class="button is-small" @click="close">Cancel</button>

</div>
</template>

<script>
export default {
  props: { 
   /* allAnalysis: {
      type: Array,
      default: () => []
    }, */
    isActive: {
      type: Boolean,
      default: false,
    }
  },
  data() {
    return {
      checked: [],
    }
  },
  computed: {
    allAnalysis() {
      return this.$store.state.analysis.all
    }
  },
  methods: {
    close() {
      this.$emit('close')
    },
    deleteSelected() {
      this.$emit('delete', this.checked)
    },
    load(event) {
      this.close()
      this.$emit('load', event)
    }
  }
}
</script>


<style>

</style>