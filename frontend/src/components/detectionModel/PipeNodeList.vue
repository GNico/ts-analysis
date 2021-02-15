<template>
<div>
  <div class="list-header">
    <span class="subtitle has-text-white"> {{ title }} </span>
    <b-dropdown scrollable :max-height="200" aria-role="list" position="is-bottom-left">
      <template #trigger="{ active }">
        <b-button
          class="is-outlined"
          label="Add Node" 
          type="is-info" 
          size="is-small"/>
      </template>

      <b-dropdown-item 
        v-for="item in nodeTypes" 
        :key="item.type"
        @click="addNode(item.type)"
        aria-role="listitem">
        {{item.display}}
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
    nodeTypes: {
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
    filteredPipenodes() {
      return this.nodes.filter(elem => elem.group === this.group)
    },
  },
  methods: {
    addNode(type) {
      this.$emit('newNode', {type: type, group: this.group})
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