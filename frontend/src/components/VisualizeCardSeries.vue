<template>

<ModalCard 
  :isActive="isActive" 
  :title="isEdit ? 'Edit Series' : 'Add Series'"
  minheight="50%"
  @close="close"
  @accept="isEdit ? updateSeries() : addSeries()">

  <div class="columns is-multiline is-marginless is-gapless is-paddingless">
    <!--first column-->
    <div class="column is-6"> 
      <div class="field is-horizontal">
        <div class="field-label is-small has-text-left">
          <label class="label">Name</label>
        </div>
        <div class="field-body">
          <div class="field is-narrow short-field">
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
          <div class="field is-narrow short-field">
            <div class="control">
              <SearchSelect 
                :saved="seriesOptions.client"
                :data="clients"
                @selected="updateSelectOptions"  
                size="is-small"
                placeholder="" 
                ref=clientselect
              />
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
              <option>areaspline</option>
              <option>spline</option>
              <option>scatter</option>
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
          <div class="field is-narrow shorter-field">
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

    <div class="column is-full">
      <div class="label is-small filters-label">Filters</div>
    </div>
    <div class="column is-6">
      <TreeSelect 
        class="filters-box"
        rootName="All tags"
        :itemsTree="allTags"
        v-model="seriesOptions.tags" 
      />
    </div>
    <div class="column is-6">
      <TreeSelect 
        class="filters-box"
        rootName="All contexts"
        :itemsTree="allContexts"
        v-model="seriesOptions.contexts" 
      />
    </div>
  </div>
</ModalCard>
</template>


<script>
import ModalCard from './ModalCard';
import ColorSelect from './inputs/ColorSelect';  
import SearchSelect from './inputs/SearchSelect.vue';
import TreeSelect from './inputs/TreeSelect.vue';

import { tagsAndContexts } from '../mixins/TagsAndContextsOptions.js';

export default {
  name: "VisualizeCardSeries",
  mixins: [tagsAndContexts],
  components: { ModalCard, SearchSelect, TreeSelect, ColorSelect },
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
        contexts: [],
        tags: [],
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
    }
  },
  methods: {
    close() {
      this.$emit('close')
    },
    changeColor(value) {
      this.seriesOptions.color = value  
    },
    updateSelectOptions(value) {
      this.seriesOptions.client = value  
      this.updateContexts(value)
      this.updateTags(value)
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
    } 
  }
}

</script>


<style scoped>

.filters-label {
  margin-top: 0.75rem;
  margin-bottom: 0.75rem;
}

.filters-box {
  padding-left: 0.5rem;
  max-height: 15rem;
  overflow-y: auto;
  width: 95%;
}

</style>