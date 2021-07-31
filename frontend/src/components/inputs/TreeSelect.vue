<template>
<div>
  <b-checkbox :value="applyFilter" @input="$emit('filterCheck', $event)"> 
    {{filterName}}
  </b-checkbox>  
  <TreeView 
    v-show="applyFilter"
    :items="fullTree" 
    :displayItems="displayTree"
    :value="normalizedValue" 
    @input="normalizedInputEmit"
    ref="rootnode"/>
</div>
</template>

<script>    
import TreeView from './TreeView.vue';

export default {
  name: "TreeSelect",
  components: { TreeView },
  props: {
    filterName: {
      type: String,
      default: 'Apply filter'
    },
    rootName: {
      type: String,
      default: 'All'
    },
    itemsTree: {
      type: Array, 
      default: () => []
    },
    value: {
      type: Array,
      default: null,
    }, 
    applyFilter: {
      type: Boolean,
      default: false,
    },
  },
  data () {
    return { 
    }
  },
  computed: {
    normalizedValue() {  
      if (!this.value) return [ "root" ]
      else return [ ...this.value ]
    },
    fullTree() {
      return { name: this.rootName, id: "root", children: this.itemsTree }
    },
    displayTree() {
      return { name: this.fullTree.name, id: this.fullTree.id, children: [] }
    }
  },
  methods: {
    normalizedInputEmit(values) {
      let event = [ ...values ] 
      if (values.length == 1 && values[0] == "root") event = null
      this.$emit('input', event) 
    }
  },
  watch: {
    itemsTree() {
      this.$refs.rootnode.forceClose()
    }
  }
}

</script>