<template>
<b-table 
  v-if="tagsCount"
  class="tags-table"
  height="200px"
  :data="tagsCount.tags"
  narrowed>
  
  <b-table-column field="tag" label="Tag" v-slot="props" width="50%">
    <span> {{props.row.tag}} </span>
  </b-table-column>

  <b-table-column field="count" label="Count" v-slot="props" width="25%" numeric>
    <span class="is-family-monospace is-size-7">        
      <strong>{{props.row.count}}</strong> ({{(props.row.count * 100 / tagsCount.total).toFixed(1)}}%)
    </span>
  </b-table-column>

</b-table> 
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
.tags-table .table {
  background-color: #001e25;
}

.tags-table td {
  word-break: break-all;
}

</style>