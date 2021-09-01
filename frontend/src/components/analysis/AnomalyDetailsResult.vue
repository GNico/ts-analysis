<template>
<div>
  <div class="is-flex">
    <div class="left-detail-field has-text-right mr-5 has-text-weight-bold has-text-grey-light">
      ID
    </div>
    <div class="right-detail-field has-text-left">
      {{anomaly.id}}
    </div>
  </div>

  <div class="is-flex">
    <div class="left-detail-field has-text-right mr-5 mb-1 has-text-weight-bold has-text-grey-light">
      From
    </div>
    <div class="right-detail-field has-text-left">
      <strong>{{anomaly.from}} </strong>({{formatDate(new Date(anomaly.from))}}) 
    </div>
  </div>

  <div class="is-flex">
    <div class="left-detail-field has-text-right mr-5 mb-1 has-text-weight-bold has-text-grey-light">
      To
    </div>
    <div class="right-detail-field has-text-left">
      <strong>{{anomaly.to}} </strong>({{formatDate(new Date(anomaly.to))}}) 
    </div>
  </div>

  <div class="is-flex">
    <div class="left-detail-field has-text-right mr-5 mb-1 has-text-weight-bold has-text-grey-light">
      Score
    </div>
    <div class="right-detail-field has-text-left">
      {{anomaly.score}}
    </div>
  </div>

  <div class="is-flex">
    <div class="left-detail-field has-text-right mr-5 mb-1 has-text-weight-bold has-text-grey-light">
      Node 
    </div>
    <div class="right-detail-field has-text-left">
      {{anomaly.source_node}}
    </div>
  </div>

  <div class="is-flex">
    <div class="left-detail-field has-text-right mr-5 mb-1 has-text-weight-bold has-text-grey-light">
      Anomaly sources
    </div>
    <div class="right-detail-field has-text-left">
      <template v-if="anomaly.source_anomalies.length">
        <div v-for="anom in anomaly.source_anomalies">
          {{anom}}
        </div>
      </template>
      <span v-else>-</span>
    </div>
  </div>
</div>
</template>

<script>
import { formatDate } from '@/utils/dateFormatter';

export default {
  props: {
    anomaly: {
      type: Object,
      default: {}
    }
  },
  computed: {
    
  },
  methods: {
   /* getTagsCount(series) {
      api.getTagsCount({
        name: series.client, 
        tags: series.tags,
        contexts: series.contexts,
        filterTags: series.filterTags,
        filterContexts: series.filterContexts,
        start: new Date(anomaly.min).toISOString(),
        end: new Date(anomaly.max).toISOString(),
      })
      .then(response => {   
        this.tagsCount[request.panelId].push({
          name: series.name, 
          total: response.data.total, 
          tags: response.data.tags_count
        })
      }) 
    }, */
    formatDate(date) {
      return formatDate(date)
    },   
  },
  watch: {
    anomaly: {
      deep: true,
      handler: function() {
        console.log("changes")
      }
    }
  },
 /* created() {
    this.getTagsCount(this.$store.getters['results/activeResults'])
  }, */  
}

</script>