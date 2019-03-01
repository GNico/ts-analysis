<template>    
<div class="bar-container  is-flex"> 

  <div class="bar-buttons">
    <a class="button is-primary " @click="isModalActive = true"> 
      Add series
    </a>
    <!-- <label class="checkbox details" v-show="activeSeries">
      <input type="checkbox">
        Show Details
    </label> -->
  </div>

  <b-modal :active.sync="isModalActive" has-modal-card>
    <SettingsSeries/>
  </b-modal>

  <div class="scroll-container">
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

.bar-container {
  padding: 1.25rem 1.25rem 0rem 1.25rem;
  background-color: #343c3d;
  border-radius: 8px;
}
  
.bar-buttons {
  margin-bottom: 1.25rem;
}

.scroll-container {
  display: flex;
  overflow: overlay;
}

.scroll-container > div {
  margin-right: 0.75rem;
  margin-bottom: 1.25rem;
}

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