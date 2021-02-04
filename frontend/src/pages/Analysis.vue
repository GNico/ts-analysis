<template>
<div class="fullh">
  <!--Analysis load modal -->
  <ModalAnalysisList 
    :isActive="loadModalActive" 
    @close="loadModalActive = false"
    @load="loadAnalysis"/>


  <!-- top bar -->
  <div class="wide-container is-flex"> 

    <div class="bar-buttons">
      <b-dropdown position="is-bottom-right">
        <template #trigger="{ active }">
          <b-button label="Open" icon-left="folder-open" size="is-small" type="is-primary" />
        </template>
        <b-dropdown-item @click="addItem">
          <div class="media">
            <b-icon class="media-left" icon="text-box-plus-outline"></b-icon>
            <div class="media-content">
                <h3>New analysis</h3>
            </div>
          </div>  
        </b-dropdown-item>
        <b-dropdown-item @click="loadModalActive = !loadModalActive">
          <div class="media">
            <b-icon class="media-left" icon="download"></b-icon>
            <div class="media-content">
                <h3>Load analysis</h3>
            </div>
          </div> 
        </b-dropdown-item>
      </b-dropdown> 
    </div>
    
    <div class="scroll-container">
      <div class="control" v-for="(item, index) in localAnalysis" :key="item.id" >
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
    <b-tabs type="is-medium is-boxed"  :animated="false" v-model="activeTab">
      <b-tab-item label="Settings" icon="cog" value="Settings" >
        <SettingsTab @run="activeTab='Results'"/>    
      </b-tab-item>
      <b-tab-item label="Results" icon="file-chart" value="Results" :disabled="!hasResults">
        <ResultsTab v-if="hasResults"/>
        <span v-else class="is-size-5"> No results yet. Run analysis first! </span>
      </b-tab-item>
    </b-tabs>
  </div>
</div>
</template>


<script>
import BarItemButton from '../components/inputs/BarItemButton';
import SettingsTab from '../components/analysis/SettingsTab';
import ResultsTab from "../components/analysis/ResultsTab";

import ModalAnalysisList from "../components/analysis/ModalAnalysisList"


export default {
  components: {  BarItemButton, SettingsTab, ResultsTab, ModalAnalysisList },
  data () {
    return {        
      activeTab: "Settings",
      loadModalActive: false,
    }
  },
  computed: {
    savedAnalysis() {
      return this.$store.state.analysis.all
    },
    localAnalysis() {
      return this.$store.state.analysis.local
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
      this.$store.dispatch("analysis/createLocalAnalysis")
    },
    loadAnalysis(id) {
      this.$store.dispatch("analysis/loadAnalysis", id)
    },
    removeItem(id) {
      this.$store.dispatch("analysis/closeLocalAnalysis", id)
    },
    toggleActive(id) {
      this.$store.dispatch("analysis/setActiveAnalysis", id)
    },
  },
  created() {
    this.$store.dispatch("analysis/fetchAllAnalysis")
  }
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
  border-top: 2px solid rgba(255,255,255,0.1);
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