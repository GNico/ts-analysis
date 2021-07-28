<template>
<div>
  <b-checkbox v-model="apply"> 
    {{filterName}}
  </b-checkbox>  
  <TreeView 
    v-if="apply"
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
      required: false,
    },
  },
  data () {
    return { 
      apply: false
    }
  },
  computed: {
    normalizedValue() {  
      if (!this.value)
        return []
      else if (this.value.length == 0 )
        return [ "root" ]
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
      if (values.length == 0) event = null
      if (values.length == 1 && values[0] == "root") event = []
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