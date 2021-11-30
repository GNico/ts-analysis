<template>
<div>
  <div class="columns test-border-ext">    
    <div class="column is-3 test-border-int">
      <div class="is-flex is-justify-content-space-between">
        <div class="label">  Test set </div>
        <b-dropdown ref="dropdown1" position="is-bottom-left" append-to-body trap-focus>
          <a
            class="button is-primary is-small is-outlined"
            slot="trigger"
            role="button">
            <span class="has-text-weight-semibold">Save</span>
          </a>
          <b-dropdown-item
            aria-role="menu-item"
            :focusable="false"
            custom
            paddingless>
            <FormSimpleName @submit="saveTestSet" buttonText="Save"/>
          </b-dropdown-item>
        </b-dropdown>        
      </div>

      <div v-if="activeTestAnomalyId" class="card mt-3">
        <div class="card-header">
          <p class="card-header-title">
            Selected
          </p>
          <button class="card-header-icon" @click="activeTestAnomalyId = ''">
            <b-icon icon="close"/>            
          </button>          
        </div>
        <div class="card-content">      
          <b-field label="From" horizontal>
            <b-datetimepicker
              :value="new Date(activeTestAnomaly.from)"
              :max-datetime="new Date(activeTestAnomaly.to)"
              @input="updateActive({from: $event.getTime()})"
              icon="calendar-today"
              size="is-small"
              editable>
            </b-datetimepicker>
          </b-field>
          <b-field label="To" horizontal>
            <b-datetimepicker
              :value="new Date(activeTestAnomaly.to)"
              :min-datetime="new Date(activeTestAnomaly.from)"
              @input="updateActive({to: $event.getTime()})"
              icon="calendar-today"
              size="is-small"
              editable>
            </b-datetimepicker>
          </b-field>

          <div class="has-text-right">
            <a class="button is-small is-danger" @click="deleteTestAnomaly">Delete</a>
          </div>
        </div>
      </div>

      <template v-else>
        <div> 
          <div class="my-2">Choose a method to define a test set</div>
          <b-field class="import-radio">
            <b-radio-button v-model="importMode" @click.native="fetchTestSets"
                native-value="load">
                Load
            </b-radio-button>
            <b-radio-button v-model="importMode"
                native-value="text">
                <span>From text</span>
            </b-radio-button>
            <b-radio-button v-model="importMode"
                native-value="file">
                <span>From file</span>
            </b-radio-button>
            <b-radio-button v-model="importMode"
                native-value="select">
                Manual selection
            </b-radio-button>
          </b-field>
        </div>

        <div v-if="importMode == 'load'" class="m-4">
          <b-table 
            :data="allTests" 
            sticky-header
            height="200px"
            narrowed
            hoverable
            :selected.sync="selectedTest"
            @dblclick="load">              
              <b-table-column field="name" label="Name" sortable>
                <template v-slot="props">
                  {{ props.row.name }}
                </template>                 
              </b-table-column>
          </b-table>

          <div class="has-text-right mt-2">
            <a class="button is-small is-danger mr-2" @click="deleteTestSet">Delete</a>
            <a class="button is-small is-info" @click="load">Load</a>
          </div>
        </div>

        <div v-if="importMode == 'text'" class="m-4">
          <b-field label="Insert anomalies">
            <b-input type="textarea" v-model="textInput"></b-input>
          </b-field>
          <div class="has-text-right">
            <a class="button is-small is-info" @click="createFromText">Create</a>
          </div>
        </div>

        <div v-if="importMode == 'file'" class="m-4">
          <b-field class="file is-info" :class="{'has-name': !!file}">
            <b-upload v-model="file" class="file-label">
              <span class="file-cta">
                <b-icon class="file-icon" icon="upload"></b-icon>
                <span class="file-label">Click to upload</span>
              </span>
              <span class="file-name" v-if="file">
                {{ file.name }}
              </span>
            </b-upload>
          </b-field>
          <div class="has-text-right" v-show="file">
            <a class="button is-small is-info" @click="createFromFile">Import</a>
          </div>
        </div>

        <div v-if="importMode == 'select'" class="m-4">
          <a class="button is-info" @click="toggleAnomalyDefinition">
            <template v-if="defineAnomaly">
              <b-icon icon="select-off"></b-icon><span>Stop selection</span>
            </template>
            <template v-else>
              <b-icon icon="select"></b-icon><span>Enable selection</span>
            </template>
          </a> 
          <a class="button is-danger" @click="clearAll">
            Clear all
          </a>
        </div>
      </template>
    </div>

    <div class="column is-9">
      <Chart       
        height="400px"
        :seriesData="seriesData"
        :anomalies="testedAnomalies"
        :activeAnomaly="activeTestAnomalyId"
        :loading="loading"   
        :showMinMax="true"
        :zoomEnabled="!selectionMode"
        :range="range"        
        @updateRange="updateRange"
        @areaSelectionChange="addTestAnomaly"
        @changeActive="activeTestAnomalyId = $event"
      />
    </div>
  </div>

  <div class="columns">    
    <div class="column is-3 test-border-int">
      <div class="is-flex is-justify-content-space-between">
        <div class="label"> Results </div>
        <div>
          <b-dropdown ref="dropdown2" position="is-bottom-left" append-to-body trap-focus>
            <a
              class="button is-primary is-small is-outlined"
              slot="trigger"
              role="button">
              <!-- <b-icon  icon=""></b-icon> -->
              <span class="has-text-weight-semibold">Save as test set</span>
            </a>
            <b-dropdown-item
              aria-role="menu-item"
              :focusable="false"
              custom
              paddingless>
              <FormSimpleName @submit="saveResultsAsTestSet" buttonText="Save"/>
            </b-dropdown-item>
          </b-dropdown> 
        </div>
      </div>

      <div> 
        <div class="my-2">Select the comparison method</div>
        <b-field>
          <b-radio-button v-model="mainCompareMode"
              native-value="strict">
              Strict
          </b-radio-button>
          <b-radio-button v-model="mainCompareMode"
              native-value="lenient">
              Lenient
          </b-radio-button>          
        </b-field>

        <template v-if="mainCompareMode =='lenient'">
          <b-field>
            <b-radio 
              size="is-small"
              v-model="lenientCompareMode"
              native-value="any">
              Any overlap
            </b-radio>
          </b-field>

          <b-field>
            <b-radio 
              size="is-small"
              v-model="lenientCompareMode"
              native-value="resultInside">
              Result anomaly inside test anomaly
            </b-radio> 
          </b-field>

          <b-field>
            <b-radio
              size="is-small"
              v-model="lenientCompareMode"
              native-value="testInside">
              Test anomaly inside result anomaly
            </b-radio>         
          </b-field>
        </template>
      </div>

      <div class="button is-small is-info my-3" @click="evaluateResults">Compare</div>
      <template v-if="metrics">
        <b-field grouped group-multiline>
          <div class="control">
            <b-taglist attached>
              <b-tag class="has-background-grey-dark has-text-white">TP</b-tag>
              <b-tag type="is-info">{{ metrics.tp }}</b-tag>
            </b-taglist>
          </div>

          <div class="control">
            <b-taglist attached>
              <b-tag class="has-background-grey-dark has-text-white">FP</b-tag>
              <b-tag type="is-link">{{ metrics.fp }}</b-tag>
            </b-taglist>
          </div>

          <div class="control">
            <b-taglist attached>
              <b-tag class="has-background-grey-dark has-text-white">FN</b-tag>
              <b-tag type="is-danger">{{ metrics.fn }}</b-tag>
            </b-taglist>
          </div>
        </b-field>

        <b-field>
          <div class="control">
            <b-taglist attached>
              <b-tag class="has-background-grey-dark has-text-white">Precision</b-tag>
              <b-tag type="is-primary">{{ formatDecimal(metrics.precision) }}</b-tag>
            </b-taglist>
          </div>
        </b-field>

        <b-field>
          <div class="control">
            <b-taglist attached>
              <b-tag class="has-background-grey-dark has-text-white">Recall</b-tag>
              <b-tag type="is-primary">{{ formatDecimal(metrics.recall) }}</b-tag>
            </b-taglist>
          </div>          
        </b-field>

        <b-field>
          <div class="control">
            <b-taglist attached>
              <b-tag class="has-background-grey-dark has-text-white">F1 score</b-tag>
              <b-tag type="is-primary">{{ formatDecimal(metrics.f1) }}</b-tag>
            </b-taglist>
          </div>          
        </b-field>
      </template>
    </div>

    <div class="column is-9">
      <Chart       
        height="400px"
        :seriesData="seriesData"
        :anomalies="anomalies"
        :loading="loading"   
        :showMinMax="true"
        :zoomEnabled="true"
        :range="range"
        @updateRange="updateRange"
      />
    </div>
  </div>
</div>
</template>


<script>
import Chart from "@/components/analysis/Chart"
import FormSimpleName from "@/components/FormSimpleName"
import api from "@/api/repository";
import { nanoid } from 'nanoid'
import cloneDeep from "lodash/cloneDeep";


const AnomaliesComparison = {
  strict: (test, result) => {
    return (test.from == result.from && test.to == result.to)
  },
  any: (test, result) => {
    return true
  },
  testInside: (test, result) => {
    return (test.from >= result.from && test.to <= result.to)
  },
  resultInside: (test, result) => {
    return (test.from <= result.from && test.to >= result.to)
  },
}
 
export default {
  components: { Chart, FormSimpleName },
  data() {
    return {
      range: {},
      testedAnomalies: [],
      activeTestAnomalyId: '',
      defineAnomaly: false,
      importMode: '',
      selectedTest: null,
      allTests: [],
      file: null,
      textInput: '',
      metrics: null,
      metricAnomalies: [],
      mainCompareMode: 'lenient',
      lenientCompareMode: 'any'
    }       
  },
  computed: {
    activeResults() {
      return this.$store.getters['results/activeResults']
    },
    loading() {
      return this.activeResults.loading
    },
    error() {
      return this.activeResults.error
    },
    resultsData() {
      return this.activeResults.results
    },      
    seriesData() {
      return !this.loading && 
            this.resultsData && 
            this.resultsData.hasOwnProperty("series") 
            ? this.resultsData.series :  [] 
    }, 
    anomalies() {
      return !this.loading &&
            this.resultsData &&      
            this.resultsData.hasOwnProperty("anomalies") ? this.resultsData.anomalies : []
    },
    activeTestAnomaly() {
      return this.testedAnomalies.find(elem => elem.id == this.activeTestAnomalyId)
    },

    selectionMode() {
      return this.defineAnomaly && this.importMode == 'select'
    },
    compareMode() {
      if (this.mainCompareMode == 'lenient') 
        return this.lenientCompareMode
     else 
        return this.mainCompareMode
    }
  },
  methods: {
    addTestAnomaly(selection) {
      if (selection) {
        const from = Math.round(selection.min)
        const to = Math.round(selection.max)    
        //check for collisions
        var collisions = this.testedAnomalies.filter(elem => {
          return (elem.from < to &&  to < elem.to) || 
              (elem.to > from && from > elem.from) ||
              (elem.from > from && elem.to < to)
        })
        var rest = this.testedAnomalies.filter(elem => {
          return !((elem.from < to &&  to < elem.to) || 
              (elem.to > from && from > elem.from) ||
              (elem.from > from && elem.to < to))
        })
        //merge 
        var lowest = from 
        var highest = to 
        collisions.forEach(elem => {
          if (elem.from < lowest)
            lowest = elem.from
          if (elem.to > highest) {
            highest = elem.to
          }
        })
        this.testedAnomalies = rest
        var id = nanoid(15)
        this.testedAnomalies.push({
          id: id,
          from: lowest,
          to: highest,
          duration: highest - lowest
        })
        this.activeTestAnomalyId = id
      }
    },
    updateRange(newRange) {
      this.range = newRange
    },
    toggleAnomalyDefinition() {
      this.defineAnomaly = !this.defineAnomaly
    },
    updateActive(opts) {
      var found = this.testedAnomalies.findIndex(elem => elem.id == this.activeTestAnomalyId)
      if (found != 1) {
        var newOpts = { ...this.testedAnomalies[found] , ...opts}
        this.testedAnomalies.splice(found, 1, newOpts)
      }
    },
    deleteTestAnomaly() {
      var found = this.testedAnomalies.findIndex(elem => elem.id == this.activeTestAnomalyId)
      if (found != 1) {
        this.testedAnomalies.splice(found, 1)
      }
      this.activeTestAnomalyId = ''
    },
    clearAll() {
      this.testedAnomalies = []
      this.activeTestAnomalyId = ''
    },
    createFromText() {
      this.testedAnomalies = JSON.parse(this.textInput)
      this.activeTestAnomalyId = ''
    },
    createFromFile() {
      const reader = new FileReader()
      reader.onload = (res) => {
        this.testedAnomalies = JSON.parse(res.target.result)
      };
      reader.onerror = (err) => console.log(err)
      reader.readAsText(this.file)
    },


    evaluateResults() {
      var i = 0, j = 0     
      const n = this.testedAnomalies.length
      const m = this.anomalies.length
      const overlapped = new Set()
      const overlappedTest = new Set()
      this.testedAnomalies.sort((a, b) => {return a.from - b.from})
      this.anomalies.sort((a, b) => {return a.from - b.from})
       
      while (i < n && j < m) {
        var l = Math.max(this.testedAnomalies[i].from, this.anomalies[j].from)
        var r = Math.min(this.testedAnomalies[i].to, this.anomalies[j].to)
        if (l <= r) {  //pair overlapping
          if (AnomaliesComparison[this.compareMode](this.testedAnomalies[i], this.anomalies[j])) {
            overlapped.add(this.anomalies[j].id)
            overlappedTest.add(this.testedAnomalies[i].id)
          }          
        }
        if (this.testedAnomalies[i].to < this.anomalies[j].to)
            i++
        else
            j++
      }

      const tp = overlapped.size
      const fp = m - tp
      const fn = n - overlappedTest.size 
      const precision = tp / (tp + fp)
      const recall = tp / (tp + fn)
      const f1 = 2 * recall * precision / (recall + precision)
      this.metrics = {tp, fp, fn, precision, recall, f1}      
    },
    formatDecimal(val) {
      return isNaN(val) ? '' : val.toFixed(2)
    },
    fetchTestSets() {
      api.getTestSetsList()
      .then(response => this.allTests = response.data)
    },
    load() {
      if (this.selectedTest && this.selectedTest.id) {
        api.getTestSet(this.selectedTest.id)
        .then(response =>  {
          this.testedAnomalies = response.data.anomalies
        })
      }
    },
    saveTestSet(form) {
      this.$refs.dropdown1.toggle()
      api.saveTestSet({name: form.name, anomalies: this.testedAnomalies})
      .then(response => this.fetchTestSets())
    },
    saveResultsAsTestSet(form) {
      this.$refs.dropdown2.toggle()
      api.saveTestSet({name: form.name, anomalies: this.anomalies})
      .then(response => this.fetchTestSets())
    },
    deleteTestSet() {
      if (this.selectedTest && this.selectedTest.id) {
        api.deleteTestSet(this.selectedTest.id)
        .then(response => this.fetchTestSets())
      }
    }
  }
}


</script>


<style>
.import-radio {
  overflow: auto;
}

.test-border-ext {
  margin-bottom: 0.75rem;
  border-bottom: 2px solid rgba(255,255,255,0.1);
}

.test-border-int {
  border-right: 2px solid rgba(255,255,255,0.1);
}
</style>