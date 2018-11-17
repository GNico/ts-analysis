<template>
<!--Grid -->
<div class="tile is-ancestor">
  <div class="tile is-vertical is-9">
  	<div class="tile is-parent">
	    <div class="tile is-child notification">
	      <div class="level">
			<div class="level-left">
				<div class="level-item">
					<label class="label">Cliente</label>

				</div>
				<div class="level-item">
			            <b-autocomplete
			                v-model="name"
			                placeholder="Seleccionar cliente"
			                open-on-focus
			                :data="filteredDataArray"
			                field="name"
			                @select="option => selected = option">
			                <template slot="empty">No results for {{name}}</template>
			            </b-autocomplete>
			     </div>

			</div>
			<div class="level-right">
				<div class="level-item">
					<label class="label">Rango</label>
				</div>
				<div class="level-item">
						<vue-ctk-date-time-picker
				            v-model="selectedRange"
				            range-mode
				            overlay-background
				            locale="es"
				            color="purple"
				            enable-button-validate
				            format="YYYY-MM-DD"
				            formatted="DD MMM YYYY"
				            label="" />	
				</div>
				<div class="level-item">
					<button class="button is-success is-medium " @click="updateRange">
						Actualizar
					</button>					
				</div>
			</div>


	      </div>

	    </div>
	</div>

	  <div class="tile">
	    <div class="tile is-parent">
	      <div class="tile is-child">
	        <MainChart></MainChart>
	      </div>
	    </div>
	  </div>
  </div>



	<div class="tile is-parent">
	  <div class="tile is-child is-danger notification">
		<p class="title">Panel de control (temporario)</p>

	  	<div class="panel-control">
		  <label class="label">Cliente</label>
				
		</div>


		<div class="panel-control">
		  <label class="label">Rango</label>
		</div>
	  </div>
	</div>

	


</div>	

</template>



<script>
	
import MainChart from '../components/MainChart.vue';
import { mapState } from 'vuex';


export default {

	components: { MainChart },

	data () {
		return {
			dropoptions: [],
			selectedRange: { 
				start: null,
				end: null 
			},
			selected: null,
			name: '',

		}
	},
	computed: {
		clients() {
      		return this.$store.state.series.clients
    	},
    	range() {
    		return this.$store.state.series.range
    	},
    	filteredDataArray() {
            return  this.clients.filter(
				(item) => {return item.name.toLowerCase().match(this.name.toLowerCase())} )
        }
	},
	methods: {
		updateRange() {
			if (selectedRange.start && selectedRange.end) {

			}
		}
	},
	watch: {
		selectedRange(newValue) {
			this.$store.commit('update_range', newValue)
		}
	}
}




</script>


<style scoped>

.actually-not-field {
	margin-bottom: -0.75rem;

}


</style>