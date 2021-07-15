<template>

<b-table 
  v-if="!isEmpty"
  :data="anomalies" 
  :selected="selected"      
  narrowed
  sticky-header
  :opened-detailed="openRows"
  detailed
  detail-key="id"
  :show-detail-icon="false"
  @select="changeActiveAnomaly($event)">

  <b-table-column field="score" label="Score" sortable numeric v-slot="props">
     <span class="tag is-info is-small">{{ props.row.score }}</span>
  </b-table-column>

  <b-table-column field="from" label="Start date" sortable centered v-slot="props">
    {{ new Date(props.row.from).toLocaleString('es-AR', {month: '2-digit', day: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit'}) }}      
  </b-table-column>
  
  <b-table-column field="to" label="End date" sortable centered v-slot="props">
    {{ new Date(props.row.to).toLocaleString('es-AR', {month: '2-digit', day: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit'}) }}
  </b-table-column>


  <template #detail="props">
    <article :id="props.row.id" class="extra has-text-centered">                    
      <p>
          <strong>{{ props.row.id }}</strong>
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
    anomalies: {
      type: Array,
      default: () => { return [] }
    },
    activeAnomaly: {
      type: String,
    },
    height: {
      type: [ Number, String ],
      default: undefined,
    }
  },
  computed: {
    selected() {
      return this.anomalies.find(item => item.id === this.activeAnomaly)
    },    
    openRows() {
      if (this.selected) {
        this.$nextTick(function () {
          var element = document.getElementById(this.activeAnomaly);
          element = element.closest('.detail').previousElementSibling
          var scrollamount = element.offsetTop
          var tableWrapper = element.closest('.table-wrapper')
          if (tableWrapper) {            
           tableWrapper.scroll(0, scrollamount - 32)
           if (! (tableWrapper.scrollHeight - tableWrapper.scrollTop === tableWrapper.clientHeight)) {
            tableWrapper.scroll(0, scrollamount -  32)
           }
          }  
        })
      }
      return this.selected ? [this.selected.id] : []
    },
    isEmpty() {
      return (!this.anomalies || !this.anomalies.length)
    }
  },
  methods: {
    changeActiveAnomaly(event) {
      this.$emit('changeActive', event.id)
    },
  }
}
</script>

