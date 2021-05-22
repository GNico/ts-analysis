<template>
<div class="p-5">
  <div class="columns is-marginless mb-4">
    <div class="column is-6-mobile is-5-widescreen is-4-fullhd  is-paddingless">
      <b-field grouped>
          <b-input expanded placeholder="Search..." size="is-small"></b-input>
          <p class="control">
            <a class="button is-primary is-small">
              <b-icon size="is-small" icon="filter-variant"></b-icon>
              <span class="has-text-weight-semibold">Filters</span>
            </a>
          </p>
      </b-field>
    </div>
    <div class="column is-paddingless">
      <div class="is-flex is-align-items-center has-text-right is-justify-content-flex-end">
        <span class="mr-2">On selected:</span> 
        <div class="field has-addons">
          <p class="control">
            <a class="button is-small is-primary" @click="performAction">{{currentAction}}</a>
          </p>
          <p class="control">
            <b-dropdown scrollable :max-height="200" aria-role="list" position="is-bottom-left">
              <template #trigger="{ active }">
                <b-button class="button-right is-shadowless" icon-left="menu-down" size="is-small" type="is-primary"/>
              </template>
              <b-dropdown-item 
                v-for="action in onSelectedActions" 
                :key="action"
                @click="currentAction = action"
                aria-role="listitem">
                {{action}}
              </b-dropdown-item>
            </b-dropdown>
          </p>
        </div>        
      </div> 
    </div>
  </div>

  <IncidentsTable :incidents="allIncidents"/>
</div>
</template>

<script>
import IncidentsTable from '@/components/monitoring/IncidentsTable'
import api from '@/api/repository'


export default {
  components: { IncidentsTable },
  data() {
    return {
      allIncidents: [],
      error: '',
      currentAction: 'Mark as closed',
      onSelectedActions: [
        'Mark as closed',
        'Mark as open',
        'Delete incident',       
      ],
    }
  },
  methods: {
    fetchIncidents() {
      return  api.getAllIncidents()
              .then(response => {
                this.error = ''
                this.allIncidents = response.data
              })
              .catch(error => this.error = 'There was an error retrieving data')
    },
    performAction() {

    }
  },
  created() {
    this.fetchIncidents()
  }
}

</script>


<style scoped>
.button-right {
  border-left: 1px solid rgba(255,255,255,0.5);
}

.button-right:focus {
  border-left: 1px solid rgba(255,255,255,0.5);
}
</style>
