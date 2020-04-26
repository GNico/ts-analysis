<template>
<div>
  <section class="section">
    <VisualizeToolBar class="char-bar"/>
    <VisualizeChart class="is-fullheight"/>
  </section>
</div>
</template>


<script>

import VisualizeChart from '../components/VisualizeChart.vue';
import VisualizeToolBar from '../components/VisualizeToolBar.vue';


export default {
  components: { VisualizeChart, VisualizeToolBar },
  data () {
    return {
      
      
    }
  },
  methods: {
    
  }

}



</script>


<style scoped>

.section {
  padding: 1rem;
}

.char-bar {
  margin-bottom: 0.75rem;
}

.is-fullheight {
  height: calc(100vh - 8.5rem);
  min-height: calc(100vh - 8.5rem);
}


</style>