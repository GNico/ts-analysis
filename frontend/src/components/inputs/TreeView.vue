<template>
<li>
    <div class="is-flex">
      <b-checkbox 
        :value="parentSelected || (isParent ? allChildLeavesSelected : value)" 
        :native-value="parentSelected || (isParent ? allChildLeavesSelected : items.id)"
        @input="checkboxEmit"
        :indeterminate="indeterminate"> 
          {{ items.name }} 
      </b-checkbox>
      <button class="transparent-button" @click="toggle">
        <b-icon :icon="isOpen ? 'chevron-up' : 'chevron-down'" size="is-small"  v-if="isParent"></b-icon> 
      </button>
    </div>

  <ul v-show="isOpen" v-if="isParent">
    <TreeView
      class="item"
      v-for="(child, index) in displayItems.children"
      :key="index"
      :items="items.children[index]"
      :displayItems="child"
      :value="value"
      :parentSelected="parentSelected || allChildLeavesSelected"
      @input="nodeEmit"
      @uncheck="uncheck"/>
  </ul>
</li>


</template>


<script>

export default {
  name: 'TreeView',
  props: {
    items: {
      type: Object,
      required: true,
      default: () => {}
    },
    displayItems: {
      type: Object,
      required: true,
      default: () => {}
    },
    value: {
      type: Array,
      required: false,
      default: null
    },
    parentSelected: {
      type: Boolean,
      required: false,
      default: false
    },
  },
  data () {
    return {
      isOpen: false
    }
  },
  computed: {
    isParent() {
      return !! this.items.children && this.items.children.length > 0
    },
    allChildLeaves() {
      let leaves = []
      let searchTree = items => {
        if (!! items.children && items.children.length > 0) {
          for (let i = 0; i < items.children.length; i++) {
            searchTree(items.children[i])
          }
        } else {
          leaves.push(items)
        }
      }
      searchTree(this.items)
      return leaves
    },
    allChildren() {
      let children = []
      let searchTree = items => {
        children.push(items)
        if (!! items.children && items.children.length > 0) {
          for (let i = 0; i < items.children.length; i++) {
            searchTree(items.children[i])
          }
        }
      }
      searchTree(this.items)
      return children
    },
    allChildLeavesSelected() {
      return  this.value.includes(this.items.id) || this.parentSelected || 
              (this.isParent && 
              (this.items.children.every(child => this.value.some(sel => sel === child.id)) ||
              this.allChildLeaves.every(leaf => this.value.some(sel => sel == leaf.id))))
    },
    indeterminate() {
      return this.isParent && this.someChildLeavesSelected && !this.allChildLeavesSelected
    },
    someChildLeavesSelected() {
      return (this.items.children.some(child => this.value.some(sel => sel === child.id)) || 
              this.allChildLeaves.some(leaf => this.value.some(sel => sel == leaf.id)))      
    }
  },
  methods: { 
    checkboxEmit(event) {
      if (this.isParent) {
        if (this.allChildLeavesSelected) {
          let ix = this.value.indexOf(this.items.id)
            if (ix > -1) {
              this.value.splice(ix, 1)
            }
          this.uncheckAllChildren()
        } else {
          this.uncheckAllChildren()
          this.value.push(this.items.id)
        }      
        //this.$emit('input', this.value)      
      }
      if (this.parentSelected) {
        this.$emit('uncheck', this.items.id)
      }
      if (this.parentSelected || this.isParent) {
        this.$emit('input', this.value)
      } else {
        this.$emit('input', event)
      }
    },
    nodeEmit(event) {
      this.$emit('input', event)
    },  
    toggle() {
      if (this.isParent) {
        let event = { id: this.displayItems.id }
        this.isOpen = !this.isOpen
        if (this.isOpen) {
          this.items['children'].forEach(child => {
            let newchild = {id: child.id, name: child.name}
            if (child.hasOwnProperty('children')) {
              newchild['children'] = []
            }
            this.displayItems['children'].push(newchild)
          })
        } else {
          this.displayItems.children = []
        }
      }
    }, 
    uncheck(childId) {
      if (this.allChildLeavesSelected) {
        // push back all children except the given one
        for (let i = 0; i < this.items.children.length; i++) {
          if (this.items.children[i].id !== childId) {
            this.value.push(this.items.children[i].id)
          }
        }
      }
      // uncheck the child
      let cix = this.value.indexOf(childId)
      if (cix > -1) {
        this.value.splice(cix, 1)
      }
      // uncheck self
      let ix = this.value.indexOf(this.items.id)
      if (ix > -1) {
        this.value.splice(ix, 1)
      }
      // propagate up
      this.$emit('uncheck', this.items.id)      
    },
    uncheckAllChildren() {
      for (let i = 0; i < this.allChildren.length; i++) {
        let ix = this.value.indexOf(this.allChildren[i].id)
        if (ix > -1) {
          this.value.splice(ix, 1)
        }
      }      
    },
  },
  watch: {
    allChildLeavesSelected(newVal) {
      if (newVal && !this.value.includes(this.items.id) && this.isParent && !this.parentSelected) {
        this.uncheckAllChildren()
        this.value.push(this.items.id)
      }
    }
  },
}

</script>

<style scoped>

.item {
  cursor: pointer;
}
.bold {
  font-weight: bold;
}
li {
  list-style-type: none;
  margin-bottom: 0.25rem;
}
ul {
  padding-left: 1em;
  line-height: 1.5em;
  margin-top: 0.25rem;

}
.transparent-button {
  background-color: Transparent;
  background-repeat:no-repeat;
  border: none;
  cursor:pointer;
  overflow: hidden;
  outline:none;
}

</style>