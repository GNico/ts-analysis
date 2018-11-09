<template>
	
<div class="tile is-ancestor">

	<div class="tile is-vertical is-6">
	  <div class="tile">
	    <div class="tile is-parent">
	      <div class="tile is-child">
	      <ClientsTable></ClientsTable>
	      </div>
	    </div>
	  </div>
	  <div class="tile is-parent">
	    <article class="tile is-child notification is-info">
	      <ClientsLoad></ClientsLoad>
	    </article>
	  </div>
	</div>

	<div class="tile is-parent">
	  <article class="tile is-child notification is-info">
	    <div class="content">
	      <p class="title">Tall tile</p>
	      <p class="subtitle">With even more content</p>
	    </div>
	  </article>
	</div>
</div>	


</template>


<script>

import ClientsTable from '../components/ClientsTable.vue';
import ClientsLoad from '../components/ClientsLoad'

export default {
	components: { ClientsTable, ClientsLoad }
}

</script>