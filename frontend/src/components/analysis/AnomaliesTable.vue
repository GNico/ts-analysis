<template>
<b-table 
  :style="{height: height}"
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
    <span class="tag is-info is-small">{{ (props.row.score * 100).toFixed(1) }}%</span>
  </b-table-column>

  <b-table-column field="from" label="Start date" sortable centered v-slot="props">
    {{ formatDate(props.row.from) }}
  </b-table-column>
  
  <b-table-column :custom-sort="sortDuration" label="Duration" sortable centered v-slot="props">
    {{ getDurationStr(getDuration(props.row)) }}
  </b-table-column>

  <template #detail="props">
    <article :id="props.row.id" class="extra has-text-centered">                    
      <p>
        <strong>{{ props.row.id }}</strong>
        <br>
        {{  props.row }}
      </p>
    </article>
  </template>
</b-table>
</template>


<script>
import { timeRangeToString, formatDateVerbose } from '@/utils/dateFormatter';

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
      default: 'inherit',
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
    formatDate(date) {
      return formatDateVerbose(date)
    },
    getDuration(anom) {
      return anom.to - anom.from
    },
    getDurationStr(timedelta) {
      return timeRangeToString(timedelta)
    },
    sortDuration(a, b, isAsc) {
      return isAsc 
        ? this.getDuration(a) < this.getDuration(b)
        : this.getDuration(a) > this.getDuration(b)
    }
  }
}
</script>


<style>
.anom-table {
  height: inherit;
}
</style>