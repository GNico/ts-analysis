<template>

<ModalCard 
  :isActive="isActive" 
  :title="isEdit ? 'Edit Series' : 'Add Series'"
  minheight="50%"
  @close="close"
  @accept="isEdit ? updateSeries() : addSeries()">

  <div class="columns is-multiline ">
    <!--first column-->
    <div class="column is-6"> 
      <div class="field is-horizontal">
        <div class="field-label is-small has-text-left">
          <label class="label">Name</label>
        </div>
        <div class="field-body">
          <div class="field is-narrow">
            <div class="control">
              <input class="input is-small" type="text" v-model="seriesOptions.name">
            </div>
          </div>
        </div>
      </div>
      <div class="field is-horizontal">
        <div class="field-label is-small has-text-left">
          <label class="label">Client</label>
        </div>
        <div class="field-body">
          <div class="field is-narrow">
            <div class="control">
             <SearchSelect
                v-model="seriesOptions.client"
                :data="clients"
                @select="clearTagsContexts"/>               
            </div>
          </div>
        </div>
      </div>
      <div class="field is-horizontal" v-if="!isEdit">
        <div class="field-label is-small has-text-left">
          <label class="label">Panel</label>
        </div>
        <div class="field-body">
          <div class="field is-narrow short-field">
            <b-select size="is-small" v-model="seriesOptions.yAxis">
              <option value="-1" default>New panel</option>
              <option v-for="index in numPanels" :key="index" :value="index-1">{{index}}</option>
            </b-select>
          </div>
        </div>
      </div>
    </div>

    <!--second column-->
    <div class="column is-6">
      <b-field class="field is-horizontal">
        <div class="field-label is-small has-text-left">
          <label class="label">Type</label>
        </div>
        <div class="field-body">
          <div class="field is-narrow short-field">
            <b-select size="is-small" v-model="seriesOptions.type">
              <option>line</option>
              <option>column</option>
              <option>area</option>
            </b-select>
          </div>
        </div>
      </b-field>
  
      <b-field class="field is-horizontal">
        <div class="field-label is-small has-text-left">
          <label class="label">Interval</label>
        </div>
        <div class="field-body">
          <div class="field is-narrow short-field">
            <div class="control">
              <b-tooltip
                label="Input must be a number followed by a valid letter [ m = minutes, h = hour, d = day ]"
                size="is-large"
                position="is-bottom"
                multilined>
                <b-input
                  v-model="seriesOptions.interval"
                  type="text"
                  size="is-small"              
                  validation-message="Invalid format"
                  pattern="[0-9]+[mhd]+">
                </b-input> 
              </b-tooltip>          
            </div>              
          </div>
        </div>
      </b-field>
      <div class="field is-horizontal">
        <div class="field-label is-small has-text-left">
          <label class="label">Color</label>
        </div>
        <div class="field-body">
          <div class="field is-narrow shorter-field">
            <div class="control">
              <ColorSelect :value="selectedColor" @input="changeColor"/>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="column is-full ">
      <div class="label is-small">Filters</div>
    </div>
    <div class="column is-6 pt-0">
      <TreeSelect 
        class="filters-box"
        filterName="Filter by tag"
        rootName="All tags"
        :applyFilter.sync="seriesOptions.filterTags"
        :itemsTree="allTags"
        v-model="seriesOptions.tags" 
        @filterCheck="seriesOptions.filterTags = $event"/>
    </div>
    <div class="column is-6 pt-0">
      <TreeSelect 
        class="filters-box"
        filterName="Filter by context"
        rootName="All contexts"
        :applyFilter="seriesOptions.filterContexts"
        :itemsTree="allContexts"
        v-model="seriesOptions.contexts" 
        @filterCheck="seriesOptions.filterContexts = $event"/>
    </div>
  </div>
</ModalCard>
</template>


<script>
import ModalCard from '../ModalCard';
import ColorSelect from '../inputs/ColorSelect';  
import TreeSelect from '../inputs/TreeSelect.vue';
import SearchSelect from '../inputs/SearchSelect.vue';

export default {
  name: "CardSeries",
  components: { ModalCard, TreeSelect, ColorSelect, SearchSelect },
  props: {
    id: {
      type: String,
      default: ''
    },
    isActive: {
      type: Boolean,
      default: false
    }
  },
  data () {
    return {
      seriesOptions: {
        name: '',
        interval: '1h',
        client: '',
        filterTags: false,
        tags: [],
        filterContexts: false,
        contexts: [],
        color: '',
        type: 'line',
        yAxis: -1,        
      },
    }
  },
  computed: {
    clients() {
      return this.$store.getters['clients/readyClients']
    },
    nextColor() {
      return this.$store.getters['visualize/nextColor']
    },
    selectedColor() {
      return this.seriesOptions.color ? this.seriesOptions.color : this.nextColor
    },
    numPanels() {
      return this.$store.getters['visualize/numPanels']
    },
    isEdit() {
      return this.id ? true : false
    },
    allTags() {
      return this.$store.state.clients.tags[this.seriesOptions.client] 
    },
    allContexts() {
      return this.$store.state.clients.contexts[this.seriesOptions.client] 
    },
  },
  methods: {
    close() {
      this.$emit('close')
    },
    changeColor(value) {
      this.seriesOptions.color = value  
    },
    addSeries() {
      this.seriesOptions.color = this.selectedColor
      this.$store.dispatch('visualize/addSeries', this.seriesOptions)
      this.resetFields()
      this.close()
    },
    updateSeries() {
      this.$store.dispatch('visualize/updateSeries', {id: this.id, seriesOptions: this.seriesOptions})
      this.close()
    },
    resetFields() {
      this.seriesOptions.name = ''
      this.seriesOptions.color = ''
      if (this.isEdit) {  //return to original from state
        this.copySeriesOptions(this.id)
      }
    },
    copySeriesOptions(seriesId) {
      const requested = this.$store.getters['visualize/getSeriesById'](seriesId) 
        for (const key of Object.keys(requested)) {
            if (this.seriesOptions.hasOwnProperty(key)) { 
                this.seriesOptions[key] = requested[key]
            }
        }
    },
    clearTagsContexts(selectevent) {
      if (selectevent[0]) {
        this.seriesOptions.tags = []
        this.seriesOptions.contexts = []
      }
    }
  },
  watch: {
    id: {
      immediate: true,
      handler(newVal) {
        if (newVal) {
          this.copySeriesOptions(newVal)
        }
      }
    },
    'seriesOptions.client': {
      handler(newVal) {
        if (!newVal || this.clients.includes(newVal)) {
          this.$store.dispatch('clients/fetchTags', (newVal))
          this.$store.dispatch('clients/fetchContexts', (newVal))
        }
      }
    }, 
  }
}

</script>


<style scoped>

.filters-box {
  padding-left: 0.5rem;
  max-height: 15rem;
  overflow-y: auto;
  width: 95%;
}

</style>