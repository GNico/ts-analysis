<template>
<div>
  <div class="list-header">
    <span class="subtitle has-text-white"> {{ title }} </span>
    <b-dropdown scrollable :max-height="200" aria-role="list">
      <template #trigger="{ active }">
        <b-button
          label="Add node" 
          type="is-primary" 
          size="is-small"/>
      </template>

      <b-dropdown-item 
        data-tooltip="test tooltip"
        v-for="item in filteredNodeSpecs" 
        :key="item.title"
        @click="addNode(item.title)"
        aria-role="listitem">
        {{item.title}}
      </b-dropdown-item>
    </b-dropdown>
  </div>

  <PipeNode 
    v-for="item in filteredPipenodes" 
    :key="item.id" 
    v-bind="item"
    :nodes="nodes"
    @nodeParamsChange="$emit('nodeParamsUpdate', $event)"
    @nodeSourceChange="$emit('nodeSourceUpdate', $event)"
    @nodeDelete="$emit('nodeDelete', $event)"/>

</div>
</template>


<script>
import PipeNode from "./PipeNode"

export default {
  components: { PipeNode },
  props: {
    title: {
      type: String,
      default: ''
    },
    type: {
      type: String,
      default: ''
    },
    nodeSpecs: {
      type: Array,
      default: () => []
    },
    nodes: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {

    }
  },
  computed: {
    filteredNodeSpecs() {
      return this.nodeSpecs.filter(elem => elem.type === this.type)
    },
    filteredPipenodes() {
      return this.nodes.filter(elem => elem.type === this.type)
    },
  },
  methods: {
    addNode(name) {
      this.$emit('newNode', name )
    }
  }

}

</script>

<style scoped>

.list-header {
  display: flex;
  justify-content: space-between;
}

</style>