<template>
<b-table 
  class="anom-table"
  :style="{height: height}"
  v-if="!isEmpty"
  :data="anomalies" 
  :selected="selected"      
  narrowed
  sticky-header
  :opened-detailed="openRows"
  :detailed="detailed"
  detail-key="id"
  :show-detail-icon="false" 
  @click="changeActiveAnomaly($event)"
>

  <b-table-column field="score" label="Score" sortable numeric v-slot="props">
    <span class="tag is-small" :style="getScoreTagStyle(props.row.score)" :id="props.row.id">
      {{ parseFloat((props.row.score * 100).toFixed(1)) }}%
    </span>
  </b-table-column>

  <b-table-column field="from" label="Start date" sortable centered v-slot="props" >
    <span class="is-family-monospace">{{ formatDateVerbose(props.row.from, true, true, true) }} </span>
  </b-table-column>
  
  <b-table-column field="duration"  label="Duration" sortable centered v-slot="props" >
     <span class="is-family-monospace"> {{ getDurationStr(props.row.duration*1000) }} </span>
  </b-table-column>

  <template #detail="props">
    <article >
      <div class="is-flex">
        <div class="left-detail-field has-text-right mr-5 has-text-weight-bold has-text-grey-light">
          ID
        </div>
        <div class="right-detail-field has-text-left">
          {{props.row.id}}
        </div>
      </div>

      <div class="is-flex">
        <div class="left-detail-field has-text-right mr-5 mb-1 has-text-weight-bold has-text-grey-light">
          From
        </div>
        <div class="right-detail-field has-text-left">
          <strong>{{props.row.from}} </strong>({{formatDate(new Date(props.row.from))}}) 
        </div>
      </div>

      <div class="is-flex">
        <div class="left-detail-field has-text-right mr-5 mb-1 has-text-weight-bold has-text-grey-light">
          To
        </div>
        <div class="right-detail-field has-text-left">
          <strong>{{props.row.to}} </strong>({{formatDate(new Date(props.row.to))}}) 
        </div>
      </div>

      <div class="is-flex">
        <div class="left-detail-field has-text-right mr-5 mb-1 has-text-weight-bold has-text-grey-light">
          Score
        </div>
        <div class="right-detail-field has-text-left">
          {{props.row.score}}
        </div>
      </div>

      <div class="is-flex">
        <div class="left-detail-field has-text-right mr-5 mb-1 has-text-weight-bold has-text-grey-light">
          Node 
        </div>
        <div class="right-detail-field has-text-left">
          {{props.row.source_node}}
        </div>
      </div>

      <div class="is-flex">
        <div class="left-detail-field has-text-right mr-5 mb-1 has-text-weight-bold has-text-grey-light">
          Anomaly sources
        </div>
        <div class="right-detail-field has-text-left">
          <template v-if="props.row.source_anomalies.length">
            <div v-for="anom in props.row.source_anomalies">
              {{anom}}
            </div>
          </template>
          <span v-else>-</span>
        </div>
      </div>
    </article>
  </template>
</b-table>
</template>


<script>
import { timeRangeToString, formatDateVerbose, formatDate } from '@/utils/dateFormatter';

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
    },
    detailed: {
      type: Boolean,
      default: true,
    }
  },
  data() {
    return {
      openRows: [],
      lastScroll: 0  //scroll control variable
    }
  },
  computed: {
    selected() {
      return this.anomalies.find(item => item.id === this.activeAnomaly)
    },    
    isEmpty() {
      return (!this.anomalies || !this.anomalies.length)
    }    
  },
  methods: {
    changeActiveAnomaly(event) {
      if (this.activeAnomaly === event.id) 
        this.$emit('changeActive', undefined)
      else 
        this.$emit('changeActive', event.id)
    },
    formatDate(date) {
      return formatDate(date)
    },

    formatDateVerbose(date, showWeekday, showTime, shortWeekdayNames) {
      return formatDateVerbose(...arguments)
    },
    getDurationStr(timedelta) {
      return timeRangeToString(timedelta)
    },
    getScoreTagStyle(score) {
      if (score <= 0.33) {
        return { 'background-color': 'dodgerblue', color: 'white', 'font-weight': 600}
      } else if (score <= 0.66) {
        return { 'background-color': 'royalblue', color: 'white', 'font-weight': 600}
      } else {
        return { 'background-color': '#005aff', color: 'white', 'font-weight': 600}
      }
    }
  },
  watch: {
    selected(newVal, oldVal) {
      if (oldRow) {
        var oldRow = document.getElementById(oldVal.id);
        var oldTr = oldRow.closest('tr')    
        console.log('scroll before', oldTr.offsetTop)
      }
      this.openRows = this.selected ? [this.selected.id] : []
      this.$nextTick(function () {
        if (this.selected) {
          var element = document.getElementById(this.selected.id);
          element = element.closest('tr')    

          console.log("scroll after:", element.offsetTop )

          var next = element.nextElementSibling
          var scrollamount = element.offsetTop - 32
          if (this.detailed && oldVal && scrollamount > this.lastScroll)
            scrollamount = scrollamount - next.clientHeight
          var tableWrapper = element.closest('.table-wrapper')
          tableWrapper.scroll({
            top: scrollamount,
            behavior: 'smooth'
          }); 
          this.lastScroll = scrollamount
        }
      }) 
    }
  }
}
</script>

<style>
.anom-table { 
  cursor: pointer;
}

.anom-table .table-wrapper {
    overflow-x: hidden;
}

.left-detail-field {
  flex: 1;
}

.right-detail-field {
  flex: 3;
}
</style>