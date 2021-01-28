<template>
<div class="container section">

  <div class="columns">
    <!-- Analysis table -->
    <div class="column is-6">
      <b-table 
        :data="analysisSettings" 
        narrowed
        sticky-header
        detailed
        detail-key="id"
        :show-detail-icon="false"
        >

        <template slot-scope="props">
          <b-table-column field="name" label="Name" sortable numeric >
             <span>{{ props.row.name }}</span>
          </b-table-column>

          <b-table-column field="description" label="Description" sortable centered>
            <span>{{ props.row.description }}</span>
          </b-table-column>
          
  

        </template>

        
      </b-table>
    </div>

    <!-- Models table -->

    <div class="column">
    </div>
  </div>
</div>

  
</template>

<script>
export default {
  data() {
    return {
      analysisSettings: [
        {
          id: 12,
          name: 'Some config',
          description: 'asd',
          data_options: {
            client_name: 'test client',
            tags: [],
            contexts: []
          }
        },


      ]
    }
  }
};
</script>


<style>

</style>