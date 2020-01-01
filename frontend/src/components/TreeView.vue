<template>
<li>
    <div class="is-flex">
      <b-checkbox 
        :value="isParent ? allChildLeavesSelected : value" 
        :native-value="isParent ? allChildLeavesSelected : items.id"
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
      @input="nodeEmit"/>
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
    }
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
          items.children.forEach(child => searchTree(child))
        } else {
          leaves.push(items)
        }
      }
      searchTree(this.items)
      return leaves
    },
    allChildLeavesSelected() {
      return this.isParent && this.allChildLeaves.every(leaf => this.value.some(sel => sel == leaf.id))
    },
    someChildLeavesSelected() {
      return this.allChildLeaves.some(leaf => this.value.some(sel => sel == leaf.id))
    },
    indeterminate() {
      return this.isParent && this.someChildLeavesSelected && !this.allChildLeavesSelected
    }
  },
  methods: {
    toggle: function () {
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
    checkboxEmit(event) {
      let t0 = performance.now()
      if (this.isParent) {
        //special case of root for optimization
       /* if (this.items.id == 'root') {
          console.log('is root')
          this.$emit('rootSelected', event)          
          return
        } */
        if (this.allChildLeavesSelected) {
          this.allChildLeaves.forEach(leaf => {
            let ix = this.value.indexOf(leaf.id)
            this.value.splice(ix,1)
          })
        } else {
          this.allChildLeaves.forEach(leaf => {
            let ix = this.value.indexOf(leaf.id)
            if (ix == -1) {
              this.value.push(leaf.id)
            }
          })
        }
        this.$emit('input', this.value)      
      } else {
        this.$emit('input', event)
      }
    let t1 = performance.now()
    console.log(t1-t0)

    },
    nodeEmit(event) {
      this.$emit('input', event)
    },  
  }
}

</script>

<style>

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
  padding-left: 2em;
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