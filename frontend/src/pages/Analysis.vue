<template>
<div class="fullh">

  <!-- top bar -->
  <div class="wide-container is-flex"> 
    <div class="bar-buttons">
      <a class="button is-primary" @click="addItem"> 
        New Analysis
      </a>   
    </div>
    <div class="scroll-container">
      <div class="control" v-for="(item, index) in analysisList" :key="item.id" >
        <BarItemButton  
          :id="item.id"
          :name="item.name ? item.name : 'Unnamed analysis'" 
          :isActive="(activeAnalysisId == item.id)"  
          @deleted="removeItem"
          @click="toggleActive"
        />
      </div>
    </div>
  </div>  

  <!-- content -->  
  <div v-show="activeAnalysisId != ''" class="wide-container main-section">
    <b-tabs type="is-toggle"  :animated="false" v-model="activeTab">
      <b-tab-item label="Settings" icon="cog" value="Settings">

        <div class="colums">
          <div class="column is-4">
            <AnalysisSettings/>
          </div>
          <div class="column">
            <BaseChart :loading="true"/>
          </div>
        </div>

      </b-tab-item>
      <b-tab-item label="Results" icon="file-chart" value="Results">
        <ResultsTab/>
      </b-tab-item>
    </b-tabs>
  </div>




</div>
</template>


<script>
//import api from "../api/repository";
import BarItemButton from '../components/BarItemButton';
import AnalysisSettings from '../components/AnalysisSettings';
import BaseChart from "../components/BaseChart";
import ResultsTab from "../components/ResultsTab";


export default {
  components: {  BarItemButton, BaseChart, AnalysisSettings, ResultsTab},
  data () {
    return {        
      activeTab: "Results",
    }
  },
  computed: {
    analysisList() {
      return this.$store.state.analysis.all
    },
    activeAnalysisId() {
      return this.$store.state.analysis.activeAnalysisId
    },
  },
  methods: {
    addItem() {
      this.$store.dispatch("analysis/createAnalysis")
    },
    removeItem(id) {
      this.$store.dispatch("analysis/removeAnalysis", id)
    },
    toggleActive(id) {
      this.$store.dispatch("analysis/setActiveAnalysis", id)
    }
  /*  getInfo(extremes) {
      api.getTagsCount({
        name: "treetest",
        start: new Date(extremes.min).toISOString(),
        end: new Date(extremes.max).toISOString(),
      })
      .then(response => {       
        this.popularTags = response.data
      })
      .catch(error => { 
        console.log('error')
        console.log(error)
      })
    } */
  },
  mounted: function () {
  },
  created() {
    
  },
}

</script>


<style scoped>

.fullh {
  height: calc(100vh - 3.5rem);
}

.wide-container {
  padding: 1.25rem 1.25rem 0rem 1.25rem;
}

.main-section {
  border-top: 2px solid rgba(255,255,255,0.05);
}

.idk {
  padding: 0;
}
  
.bar-buttons {
  margin-bottom: 1.25rem;
  margin-right: 1rem;
}

.scroll-container {
  display: flex;
  flex-wrap: wrap;
  overflow: overlay;
}

.scroll-container > div {
  margin-right: 0.75rem;
  margin-bottom: 1.25rem;
}


</style>