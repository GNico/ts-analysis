<template>
<div>
  <div v-for="tagsCount, index in tagsCountList" class="card tag-count-card mb-3">
    <header class="card-header">
      <p class="card-header-title has-text-grey-light has-text-weight-medium">
       <b v-if="tagsCountList.length > 1">{{index+1}} -&nbsp;</b> 
       <b> Tags count from {{formattedAnomalyRange}}</b>       
      </p>
      <a href="#" class="card-header-icon" aria-label="more options">
      <span class="icon">
        <i class="fa fa-angle-down" aria-hidden="true"></i>
      </span>
      </a>
    </header>
    <div class="card-table">
      <div class="content">
        <table class="table is-fullwidth is-striped">
          <tbody v-if="tagsCount">
            <tr v-for="item in tagsCount.tags">
              <td>
                <div class="is-flex is-justify-content-space-between is-family-monospace is-size-7">
                  <div class="tag-label"><i class="mdi mdi-tag-multiple"></i> {{ item.tag}}</div>
                  <div class="tag-count has-text-right has-text-weight-bold"> 
                    {{item.count}}
                    <span class="has-text-weight-medium">({{(item.count * 100 / tagsCount.total).toFixed(1)}}%)</span>
                  </div>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</div>
</template>

<script>
import api from "@/api/repository";
import { formatDateRange } from '@/utils/dateFormatter';

export default {
  props: {    
    settings: {
      type: Object,
      default: {}
    }
  },
  data() {
    return {
      tagsCountList: [],
    }
  },
  computed: {
    formattedAnomalyRange() {
      return formatDateRange(this.settings.anomalyStart, this.settings.anomalyEnd)
    }
  },
  methods: {
   getTagsCount() {
      this.tagsCountList = []
      this.settings.data_options.forEach(elem => {
        api.getTagsCount({
          name: this.settings.client,
          tags: elem.tags,
          contexts: elem.contexts,
          filterTags: elem.filterTags,
          filterContexts: elem.filterContexts,
          start: this.settings.anomalyStart,
          end: this.settings.anomalyEnd
        })
        .then(response => {   
          this.tagsCountList.push({            
            client: this.settings.client, 
            total: response.data.total, 
            tags: response.data.tags_count
          })
        })
      })      
    }, 
  },
  watch: {    
    settings: {
      immediate: true,
      handler() {
       this.getTagsCount()
      }
    }
  },
}
</script>


<style>
.tag-count-card .card-table {
  max-height: 350px;
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