<template>
<b-table 
  :data="clients" 
  detailed
  :opened-detailed="openRows"
  detail-key="name"
  :show-detail-icon="false"
  striped>       

  <template slot-scope="props">
    <b-table-column field="name" label="Client">
      {{ props.row.name }}
    </b-table-column>

    <!--Row when indexing-->
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

    <!--Row when not indexing-->
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

  <!--Row details-->
  <template slot="detail" slot-scope="props">
    <article class="extra has-text-centered">                    
      <p>
          <strong>{{ props.row.name }}</strong>
          <br>
          {{ props.row }}
      </p>
    </article>
  </template>  
</b-table>

</template>


<script>

export default {
  props: {
    clients: {
      type: Array,
      default: () => []
    }
  }

}

</script>