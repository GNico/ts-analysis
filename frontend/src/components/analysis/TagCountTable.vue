<template>
<div>
  <div class="mb-3">
    <p class="has-text-grey-light has-text-weight-medium">
       <b> Tag count from {{formattedAnomalyRange}} </b>       
    </p>
    <b-dropdown  class="header-item" aria-role="list" :value="compareTo" @input="onModeChange">
        <template #trigger>
          <a class="is-flex is-align-items-center has-text-grey">
            <b-icon icon="menu-down" class="has-text-link"></b-icon>
            <span><strong class="has-text-link">Compare to: {{compareModes[compareTo]}}</strong></span>
          </a>
        </template>
        <b-dropdown-item v-for="mode in Object.keys(compareModes)" :value="mode" :key="mode">{{compareModes[mode]}}</b-dropdown-item>
    </b-dropdown>
  </div>
  <div v-for="tagsCount, index in tagCountListWithComparison">
    <div class="card tag-count-card mb-3">
      <header class="card-header"  v-if="tagCountListWithComparison.length > 1">
        <p class="card-header-title has-text-grey-light has-text-weight-semibold">Input {{index+1}}</p>        
      </header>
      <div class="card-table" :style="tableHeight">
        <div class="content">
          <table class="table is-fullwidth is-striped">
            <tbody v-if="tagsCount">
              <tr v-for="item in tagsCount.tags">
                <td>
                  <div class="is-flex is-justify-content-space-between is-family-monospace is-size-7">
                    <div class="tag-label"><i class="mdi mdi-tag-multiple"></i> {{ item.tag}}</div>
                    <div class="tag-count has-text-right has-text-weight-bold"> 
                      {{item.count}}
                      <span class="has-text-weight-medium">({{ getItemCountPercent(item, tagsCount) }}%)</span>
                    </div>
                  </div>
                  <div v-if="compareTo" class="is-flex is-justify-content-space-between is-family-monospace is-size-7 has-text-link">      
                    <template v-if="item.comparedCount">
                      <div v-if="getItemCountDifference(item, tagsCount).val > 0" class="has-text-weight-bold has-text-success">
                        <span class="tag-label"><i class="mdi mdi-arrow-up-thick"></i> {{ getItemCountDifference(item, tagsCount).text  }}</span>
                      </div>
                      <div v-else class="has-text-weight-bold has-text-warning">
                        <span class="tag-label"><i class="mdi mdi-arrow-down-thick"></i> {{ getItemCountDifference(item, tagsCount).text  }}</span>
                      </div>                  
                      <div>
                        {{item.comparedCount}} ({{ getItemComparedCountPercent(item, tagsCount) }}%)
                      </div>
                    </template>
                    <span v-else>-</span>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</div>
</template>


<script>
import api from "@/api/repository";
import { formatDateRange } from '@/utils/dateFormatter';
import cloneDeep from 'lodash/cloneDeep'

export default {
  props: {    
    settings: {
      type: Object,
      default: {}
    },
    compareTo: {
      type: String,
      default: ''
    },
    selectionRange: {
      type: Object,
      default: null
    },
    maxHeight: {
      type: Number,
      default: 350,
    }
  },
  data() {
    return {
      tagsCountList: [],
      tagsCompareList: [],
      compareModes: {
        '': 'None',
        all: 'All time',
        before: 'Before anomaly',
        selection: 'Selection'
      }
    }
  },
  computed: {
    tableHeight() {
      let h = this.maxHeight - 50
      return {
        'max-height': `${h}px`,
      }
    },
    formattedAnomalyRange() {
      return formatDateRange(this.settings.anomalyStart, this.settings.anomalyEnd)
    },
    tagCountListWithComparison() {
      var formattedTagCountList = []
      if (!this.tagsCompareList.length) return this.tagsCountList
      for (let i = 0; i < this.tagsCountList.length; i++) {
        var input = this.tagsCountList[i] 
        var newInput = {
          client: input.client,
          total: input.total,
          comparedTotal: this.tagsCompareList[i].total,
          tags: cloneDeep(input.tags)
        }
        formattedTagCountList.push(newInput)
        if (this.tagsCompareList[i].tags) {
          newInput.tags.forEach(elem => {
            var found = this.tagsCompareList[i].tags.find(comp => comp.tag == elem.tag)
            if (found) {
              elem.comparedCount = found.count
            } else {
              elem.comparedCount = 0
            }
          })    
        } 
      } 
      return formattedTagCountList
    } 
  },
  methods: {
    fetchData() {
      this.tagsCountList = this.getTagsCount(this.settings.anomalyStart, this.settings.anomalyEnd)
      this.tagsCompareList = this.getTagsCompared()
    },
    getTagsCount(start, end) {
      var tagsCount = []
      this.settings.data_options.forEach(elem => {
        api.getTagsCount({
          name: this.settings.client,
          tags: elem.tags,
          contexts: elem.contexts,
          filterTags: elem.filterTags,
          filterContexts: elem.filterContexts,
          start: start,
          end: end,
          size: 30,
        })
        .then(response => {   
          tagsCount.push({            
            client: this.settings.client, 
            total: response.data.total, 
            tags: response.data.tags_count
          })
        })
      }) 
      return tagsCount     
    }, 
    getTagsCompared() {
      switch (this.compareTo) {
        case 'all':
          return this.getTagsCount(null, null)
        case 'before': 
          return this.getTagsCount(null, this.settings.anomalyStart)         
        case 'selection': 
          if (this.selectionRange) {
            let from = new Date(this.selectionRange.min).toISOString()
            let to =  new Date(this.selectionRange.max).toISOString()
            return this.getTagsCount(from, to)   
          } else {
            return []
          }
        default:
          return []
      }
    },
    getItemCountPercent(item, tagsCount) {
      return (item.count * 100 / tagsCount.total).toFixed(1)
    },
    getItemComparedCountPercent(item, tagsCount) {
      return (item.comparedCount * 100 / tagsCount.comparedTotal).toFixed(1)
    },
    getItemCountDifference(item, tagsCount) {
      var diff = (this.getItemCountPercent(item, tagsCount) - this.getItemComparedCountPercent(item, tagsCount)).toFixed(1)
      var text = ''
      if (diff > 0)      
        text = diff + '%'
      else if (diff < 0) 
        text = Math.abs(diff) + '%'
      return {val: diff, text: text}
    },
    onModeChange(event) {
      this.$emit('compareChange', event)
    }
  },
  watch: {    
    settings: {
      immediate: true,
      handler() {
        this.fetchData()
      }
    },   
    compareTo() {
      this.fetchData()
    },
    selectionRange() {
      if (this.compareTo == 'selection') {
        this.fetchData()
      }
    }
  },
}
</script>


<style>
.tag-count-card .card-table {
  overflow-y: auto;
  overflow-x: auto;
}

.tag-label {
  word-break: break-all;
  width: 70%;
}

.tag-count {
  width: 30%;
}

.tag-count-card .table.is-striped tbody tr:not(.is-selected):nth-child(2n-1) {
  background-color: #001e25;
}

.tag-count-card .table.is-striped tbody tr:not(.is-selected):nth-child(2n) {
  background-color: rgba(18, 18, 18, 0.1);
}
</style>