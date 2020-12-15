<template>
<TreeView 
  :items="fullTree" 
  :displayItems="displayTree"
  :value="value" 
  @input="(event) => $emit('input', event)" />
</template>


<script>    
import TreeView from './TreeView.vue';

export default {
  name: "TreeSelect",
  components: { TreeView },
  props: {
    rootName: {
      type: String,
      default: 'All'
    },
    itemsTree: {
      type: Array, 
      default: []
    },
    value: {
      type: Array,
      required: false,
      default: null
    },
  },
  data () {
    return { 
    }
  },
  computed: {
    fullTree() {
      return { name: this.rootName, id: "root", children: this.itemsTree }
    },
    displayTree() {
      return { name: this.fullTree.name, id: this.fullTree.id, children: [] }
    }
  },
  methods: {
  },
}

</script>