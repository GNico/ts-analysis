<template>

<div class="section">
  <template v-for="testcase in testcases">
    <TestCaseChart :chartData="testcase"/>
    <hr>
  </template>
</div>


</template>



<script>
import TestCaseChart from '../components/TestCaseChart.vue';
import api from "../api/repository";


export default {
  components: { TestCaseChart },
  data() {
    return {
      testcases: {},
    }
  },
  computed: {

  },
  methods: {

  },
  mounted: function () {
    let source = this.$route.query.source
    api.testAlgo(source)
      .then(response => {
        this.testcases = response.data.testcases
      })
      .catch(error => {
        console.log('Error retrieving testcases:', error)
      })
  }

}

</script>



<style scoped>

.section {
  padding: 1rem;
}

</style>