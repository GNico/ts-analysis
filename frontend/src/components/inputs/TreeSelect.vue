<template>
<TreeView 
  :items="fullTree" 
  :displayItems="displayTree"
  :value="normalizedValue" 
  @input="normalizedInputEmit"/>
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
    },
  },
  data () {
    return { 

    }
  },
  computed: {
    //@input="(event) => $emit('input', event)"
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
      console.log(values)
      let event = [ ...values ] 
      if (values.length == 0) event = null
      if (values.length == 1 && values[0] == "root") event = []
      this.$emit('input', event) 
    }
  },
}

</script>