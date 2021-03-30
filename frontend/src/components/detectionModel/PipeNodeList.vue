<template>
<div>
  <div class="notices is-top" :class="isDescriptionVisible ? '' : 'is-hidden'">
    <div role="alert" class="toast is-info is-top" style="">
      <div><strong class="has-text-white">{{display}}: </strong>{{ description }}</div>
    </div>
  </div>

  <div class="is-flex is-justify-content-space-between mb-4">
    <span class="is-size-5 has-text-white"> {{ title }} </span>
    <b-dropdown scrollable :max-height="200" aria-role="list" position="is-bottom-left">
      <template #trigger="{ active }">
        <b-button
          class="is-outlined"
          label="Add Node" 
          type="is-info" 
          size="is-small"/>
      </template>

      <b-dropdown-item 
        v-for="item in nodesDefinition" 
        :key="item.type"
        @click="addNode(item.type)"
        @mouseover.native="showDesc(item)"
        @mouseleave.native="hideDesc()"
        aria-role="listitem">
        {{item.display}}
      </b-dropdown-item>
    </b-dropdown>
  </div>

  <PipeNode 
    v-for="item in filteredPipenodes" 
    :key="item.id" 
    :id="item.id"
    :nodes="nodes"
    :nodeDefiniton="getNodeDef(item.type)"
    @nodeParamsChange="$emit('nodeParamsUpdate', $event)"
    @nodeSourceChange="$emit('nodeSourceUpdate', $event)"
    @nodeDelete="$emit('nodeDelete', $event)"
    @mouseover.native="showDesc(item)"
    @mouseleave.native="hideDesc()">
  </PipeNode>

</div>
</template>


<script>
import PipeNode from "./PipeNode";

export default {
  components: { PipeNode },
  props: {
    group: {
      type: String,
      default: ''
    },
    nodesDefinition: {
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
      isDescriptionVisible: false,
      display: '',
      description: '',
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
    },
    getNodeDef(type) {
      return this.nodesDefinition.find(item => item.type === type)
    },
    getNode(id) {
      return this.nodes.find(item => item.id === id)
    },
    showDesc(item) {
      this.display = item.display 
      this.description = item.desc
      this.isDescriptionVisible = true
    },
    hideDesc() {
      this.isDescriptionVisible = false
    }
  }
}
</script>
