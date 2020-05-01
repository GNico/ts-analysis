<template>
<div>
  <section class="section">
    <VisualizeToolBar class="char-bar"/>
    <VisualizeChart 
      class="is-fullheight"
      :series="series"/>
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
      /*[ {
          name: 'Pepega',
          data: [
          [
              1524058200000,
              177.84
          ],
          [
              1524144600000,
              172.8
          ],
          [
              1524231000000,
              165.72
          ],
          [
              1524490200000,
              165.24
          ],
          [
              1524576600000,
              162.94
          ]],
          yAxis: 0,
        },
        {
          name: 'Other',
          data:  [
          [
              1524058200000,
              176.57
          ],
          [
              1524144600000,
              176.89
          ],
          [
              1524231000000,
              183.83
          ],
          [
              1524490200000,
              185.16
          ],
          [
              1524576600000,
              186.05
          ]],
          yAxis: 1,
        },
        {
          name: 'Third',
          data: [
          [
              1524058200000,
              163.65
          ],          
          [
              1524144600000,
              164.22
          ],
          [
              1524231000000,
              162.32
          ],
          [
              1524490200000,
              165.26
          ],
          [
              1524576600000,
              169.1
          ]],
          yAxis: 2,
        }]  */
      
    }
  },
  computed: {
    series() {
      return this.$store.getters['visualize/seriesAsList']
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