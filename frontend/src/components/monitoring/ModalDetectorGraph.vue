<template>

<ModalCard 
  :isActive="isActive" 
  @close="close"
  :title="title">
  <GraphDataProvider :nodes="model">
    <LayeredGraphChart slot-scope="{chartNodes, chartEdges}" :nodes="chartNodes" :edges="chartEdges"/>
  </GraphDataProvider>
  <template v-slot:footer-right>
    <div>
      <button class="button is-small" @click="close">Close</button>
    </div>
  </template>

</ModalCard>


</template>


<script>
import ModalCard from '@/components/ModalCard'
import GraphDataProvider from '@/components/detectionModel/GraphDataProvider'
import LayeredGraphChart from '@/components/detectionModel/LayeredGraphChart'

export default {
  components: { ModalCard, GraphDataProvider, LayeredGraphChart },
  props: {
    model: {
      type: Array,
      default: () => []
    },
    isActive: {
      type: Boolean,
      default: false
    },
    title: {
      type: String,
      default: 'Detection model'
    },
    minheight: {
      type: String,
      default: '',
    },   
    minwidth: {
      type: String,
      default: '',
    },

  },
  data() {
    return {

    }
  },
  methods: {
    close() {
      this.$emit('close')
    },
  }

}
</script>