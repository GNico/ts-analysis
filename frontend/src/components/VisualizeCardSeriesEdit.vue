<template>
<div class="card">
  <header class="card-header">
    <p class="card-header-title">
      Series settings
    </p>    
  </header>

  <div class="card-content">
    <div class="field is-horizontal">
      <div class="field-label is-normal">
        <label class="label">Name</label>
      </div>
      <div class="field-body">
        <div class="field is-narrow">
          <div class="control">
            <input class="input is-small" type="text" >
          </div>
        </div>
      </div>
    </div>


    <div class="field is-grouped is-grouped-right">
      <p class="control">
        <a class="button is-primary is-small" >
          OK
        </a>
      </p>
      <p class="control">
        <a class="button is-danger is-small" @click="close">
          Cancel
        </a>
      </p>
    </div>

  </div>         
</div>
</template>


<script>

import SearchSelect from './SearchSelect.vue';
import TreeView from './TreeView.vue';

export default {
  name: 'VisualizeCardSeriesEdit',
  components: { SearchSelect, TreeView },
  data () {
    return {
      
    }
  },
  computed: {
    clients() {
      return this.$store.getters['clients/readyClients']
    },
  },
  methods: {
    close() {
      this.$emit('close')
    },

  },
  watch: {

  }
}

</script>


<style scoped>

.custom-field {
  margin-top: 0.5rem;
}

</style>