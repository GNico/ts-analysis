<template>
<div class="fullh">
  <!-- top bar -->
  <div class="wide-container is-flex"> 
    <div class="bar-buttons">
      <a class="button is-primary is-small" @click="addItem"> 
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
          @click="toggleActive"/>
      </div>
    </div>
  </div>  
  <!-- content -->  
  <div v-show="activeAnalysisId != ''" class="wide-container main-section">
    <b-tabs type="is-toggle"  :animated="false" v-model="activeTab" >
      <b-tab-item label="Settings" icon="cog" value="Settings" >
        <div class="colums">
          <div class="column is-3">
            <AnalysisSettings @run="activeTab='Results'"/>
          </div>
          <div class="column">
            <BaseChart :loading="true"/>
          </div>
        </div>
      </b-tab-item>
      <b-tab-item label="Results" icon="file-chart" value="Results" :disabled="!hasResults">
        <AnalysisResultsTab v-if="hasResults"/>
        <span v-else> No results yet. Run analysis first! </span>
      </b-tab-item>
    </b-tabs>
  </div>
</div>
</template>


<script>
import BarItemButton from '../components/BarItemButton';
import AnalysisSettings from '../components/AnalysisSettings';
import BaseChart from "../components/BaseChart";
import AnalysisResultsTab from "../components/AnalysisResultsTab";

export default {
  components: {  BarItemButton, BaseChart, AnalysisSettings, AnalysisResultsTab},
  data () {
    return {        
      activeTab: "Settings",
    }
  },
  computed: {
    analysisList() {
      return this.$store.state.analysis.all
    },
    activeAnalysisId() {
      //this.activeTab = "Settings"
      return this.$store.state.analysis.activeAnalysisId
    },
    hasResults() {
      let res = this.$store.getters['analysis/getResultsById'](this.activeAnalysisId) 
      return Object.keys(res).length != 0
    }
  },
  methods: {
    addItem() {
      this.activeTab="Settings"
      this.$store.dispatch("analysis/createAnalysis")
    },
    removeItem(id) {
      this.$store.dispatch("analysis/removeAnalysis", id)
    },
    toggleActive(id) {
      this.$store.dispatch("analysis/setActiveAnalysis", id)
    },
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