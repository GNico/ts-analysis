<template>
<!--Grid -->
<div class="tile is-ancestor">
	<div class="tile is-vertical is-8">
	  <div class="tile">
	    <div class="tile is-parent">
	      <div class="tile is-child is-info">
	        <main-chart></main-chart>
	      </div>
	    </div>
	  </div>
	  <div class="tile is-parent">
	    <article class="tile is-child notification is-danger">
	      <p class="title">Wide tile</p>
	      <p class="subtitle">Aligned with the right tile</p>
	      <div class="content">
	        <!-- Content -->
	      </div>
	    </article>
	  </div>
	</div>
	<div class="tile is-parent">
	  <article class="tile is-child notification is-success">
	    <div class="content">
	      <p class="title">Tall tile</p>
	      <p class="subtitle">With even more content</p>
	    </div>
	  </article>
	</div>
	</div>
</div>	

</template>



<script>
	
import MainChart from '../components/MainChart.vue';


export default {

	components: { MainChart }

}




</script>