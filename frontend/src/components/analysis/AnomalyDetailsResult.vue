<template>
<div>
  <div class="card tag-count-card">
    <header class="card-header">
      <p class="card-header-title has-text-grey-light">Tag counts from {{formatDate(anomaly.from)}} to {{formatDate(anomaly.to)}}</p>
      <a href="#" class="card-header-icon" aria-label="more options">
      <span class="icon">
        <i class="fa fa-angle-down" aria-hidden="true"></i>
      </span>
      </a>
    </header>
    <div class="card-table">
      <div class="content">
        <table class="table is-fullwidth is-striped">
          <tbody>
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
import { formatDate } from '@/utils/dateFormatter';

export default {
  props: {
    anomaly: {
      type: Object,
      default: {}
    }
  },
  data() {
    return {
      tagsCount: undefined,
    }
  },
  computed: {
    active() {
      return this.$store.getters['results/activeResults']
    }
  },
  methods: {
   getTagsCount(results) {
      api.getTagsCount({
        name: results.settings.client, 
        tags: results.settings.tags,
        contexts: results.settings.contexts,
        filterTags: results.settings.filterTags,
        filterContexts: results.settings.filterContexts,
        start: new Date(this.anomaly.from).toISOString(),
        end: new Date(this.anomaly.to).toISOString(),
      })
      .then(response => {   
        this.tagsCount = {
          client: results.settings.client, 
          total: response.data.total, 
          tags: response.data.tags_count
        }
      }) 
    }, 
    formatDate(date) {
      return formatDate(date)
    },   
  },
  watch: {    
  },
  created() {
    this.getTagsCount(this.$store.getters['results/activeResults'])
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