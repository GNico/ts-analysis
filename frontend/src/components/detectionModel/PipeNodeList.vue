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
        v-for="item in filteredNodeSpecs" 
        :key="item.type"
        @click="addNode(item.type)"
        aria-role="listitem">
        {{item.type}}
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
    group: {
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
    title() {
      if (!this.group) return ''
      return this.group.charAt(0).toUpperCase() + this.group.slice(1) + 's'
    },
    filteredNodeSpecs() {
      return this.nodeSpecs.filter(elem => elem.group === this.group)
    },
    filteredPipenodes() {
      return this.nodes.filter(elem => elem.group === this.group)
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