<template>    
<div class="is-flex box"> 

  <div class="bar-buttons">
    <a class="button is-primary " @click="isModalActive = true"> 
      Add series
    </a>
    <label class="checkbox details" v-show="activeSeries">
      <input type="checkbox">
        Show Details
    </label>
  </div>

  <b-modal :active.sync="isModalActive" has-modal-card>
    <SettingsSeries/>
  </b-modal>

  <div class="field is-grouped is-grouped-multiline">
    <div class="control" v-for="(item, index) in seriesNames" :key="item" >
      <ButtonSeriesName  
        :name="item" 
        @deleted="removeItem"
        @click="toggleActive"
        :isActive="(activeSeries == item)"  
      />
    </div>
  </div>
</div>    
</template>


<script>
import ButtonSeriesName from './ButtonSeriesName.vue';
import SettingsSeries from './SettingsSeries.vue';

export default {
  props: {
    activeSeries: {
      required: true,
      type: String,
    }
  }, 
  data() {
    return {
      isModalActive: false
    }
  },
  components: { ButtonSeriesName, SettingsSeries },
  computed: {
    seriesNames() {
      return this.$store.getters['series/getSeriesNames']
    },
  },
  methods: {
    removeItem(name) {
      this.$store.dispatch('series/deleteSeries', name )
    },
    toggleActive(event) {
      this.$emit('change', event)
    }
  }

}
</script>


<style>
  
.bar-buttons {
  display: flex;
  flex-direction: column;
  margin-right: 1rem;
  justify-content: space-between;
}

.details {
  margin-top: 1rem;
}

</style>