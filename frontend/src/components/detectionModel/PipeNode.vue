<template>
  <b-collapse
    class="card"
    animation="slide"
    :open="false">
    <template #trigger="props">
      <div class="card-header" @mouseover="showDelete = true" @mouseleave="showDelete = false" >
        <span class="card-header-title long-text-with-ellipsis">
          <span v-if="showDelete" class="tag is-danger header-id-tag" style="{padding: 0}" @click="deleteNode(id)"> &nbsp;X&nbsp; </span>
          <span v-else class="tag is-info header-id-tag" > {{id}} </span>
          <span class="has-text-grey-light">{{nodeDefiniton.display}} </span>
        </span>
        <a class="card-header-icon">
          <b-icon :icon="props.open ? 'menu-up' : 'menu-down'"/>
        </a>
      </div>
    </template> 

    <div class="card-content">
      <div class="content">
        <div class="is-flex">
          <b-dropdown
            append-to-body
            :value="nodeData.sources"
            @change="sourceNodesChange"
            :multiple="allowMultiple"
            aria-role="list">
            <template #trigger>
              <b-tag
                class="button is-outlined"
                size="is-small"             
                icon-right="menu-down">
                Input node
                <b-icon size="is-small" icon="menu-down"/>
              </b-tag>
            </template>
            <b-dropdown-item value='none' v-if="!allowMultiple">
              <span> None </span>
            </b-dropdown-item>
            <b-dropdown-item v-for="nodeid in sourceNodesList" :key="nodeid" :value="nodeid" aria-role="listitem">
              <span>{{getNode(nodeid).display}} (ID: {{nodeid}})</span>            
            </b-dropdown-item>
          </b-dropdown>

          <div class="node-list">
            <template v-if="nodeData.sources.length">
              <div v-for="nodeid in nodeData.sources">
                <span class="long-text-with-ellipsis">
                  <span class="tag has-background-grey-dark has-text-grey-light header-id-tag" > {{nodeid}} </span>
                  <span>{{getNode(nodeid).display}} </span>
                </span>      
              </div>      
            </template>
          </div> 
        </div>

        <hr v-if="paramsComponents.length" class="separator">

        <div class="columns is-marginless is-paddingless is-vcentered" v-for="param in paramsComponents" 
            v-if="checkConditions(param.conditions)"
            :key="param.id">
            <div class="column is-6 field-col">
              <label class="label">
                {{param.display}} 
                <b-tooltip type="is-info" :label="param.desc">
                  <b-icon size="is-small" icon="help-circle-outline"></b-icon>
                </b-tooltip>
              </label>
            </div> 
            <div class="column is-6 field-col right-align">
              <component
                class="short-field is-marginless" 
                :is="param.component.name"
                v-bind="param.component.props"
                :value="nodeData.paramsData[param.id]"
                @input="paramsDataChange(param.id, $event)">

                <option
                  v-for="option in param.options"
                  :value="option.code"
                  :key="option.code">
                  {{ option.display }}
                </option>
              </component>
            </div> 
        </div>
      </div>
    </div>
  </b-collapse>
</template>


<script>
export default {
  props: {
    id: {
      type: String,
      default: ''
    },
    nodes: {
      type: Array,
      default: () => []
    },
    nodeDefiniton: {
      type: Object,
      default: () => {
        return {
          type: '',
          desc: '',
          display: '',
          params: '',
      }}
    },
  },
  data() {
    return {
      showDelete: false,
    }
  },
  computed: {
    nodeData() {
      return this.nodes.find(elem => elem.id == this.id)
    },
    paramsComponents() {
      let components = []
      this.nodeDefiniton.params.forEach(elem => {
        components.push({
          ...elem,
          component: this.getFieldComponent(elem),
        })
      })
      return components
    },
    sourceNodesList() {
      let id = this.id
      if (this.nodeData.group === 'detector' ||  this.nodeData.group === 'transformer')
        return this.nodes.filter(elem => elem.id !== this.id && elem.group === 'transformer').map(elem => elem.id)
      if (this.nodeData.group === 'aggregator') {
        return this.nodes.filter(elem => elem.id !== this.id && (elem.group === 'detector' || elem.group === 'aggregator')).map(elem => elem.id)
      }
    },
    allowMultiple() {
      return this.nodeData.group === 'aggregator'
    }
  },
  methods: {
    checkConditions(conditions) {
      if (!conditions || !conditions.length) return true
      let evaluation = []
      conditions.forEach(cond => {
        if (cond.type == "param_equals_value") {
          evaluation.push(this.nodeData.paramsData[cond.args.param] ===  cond.args.value)
        }
      }) 
      return evaluation.every(Boolean)
    }, 
    getFieldComponent(param) {
      switch (param.type) {
        case 'Select': 
          return {
            name: 'b-select',
            props: {
              size: 'is-small',
            }
          }
        case 'Float': 
          return {
            name: 'b-input',
            props: {
              type: 'number',
              step: 0.01,
              size: 'is-small',
            }
          }
        case 'BoundedFloat': 
          return {
            name: 'b-input',
            props: {
              type: 'number',
              step: 0.01,
              max: param.max,
              min: param.min,
              size: 'is-small',
            }
          }
        case 'BoundedInt':
          return {
            name: 'b-input',
            props: {
              type: 'number',
              step: 1,
              max: param.max,
              min: param.min,
              size: 'is-small',
            }
          }
        case 'Boolean':
          return {
            name: 'b-checkbox',
            props: {    
            }
          }
        default:
          return {
            name: 'b-input',
            props: {
              type: 'text',
              size: 'is-small',
            }
          }      
        }
    },
    paramsDataChange(name, event) {
      const parsed = parseFloat(event)
      this.$emit('nodeParamsChange', {id: this.id, [name]: (isNaN(parsed) ? event : parsed)})
    },
    sourceNodesChange(event) {
      let sourceNodes = event
      if (sourceNodes === 'none') {
        sourceNodes = []
      }
      else if (!this.allowMultiple) {
        sourceNodes = [ event ]
      }
      this.$emit('nodeSourceChange', {id: this.id, sources: sourceNodes} )
    },
    deleteNode() {
      this.$emit('nodeDelete', this.id)
    },
    getNode(id) {
      return this.nodes.find(item => item.id === id)
    }
  }
}
</script>



<style scoped>
.field-col {
  padding: 0;
  margin: 0.25rem;
}

.right-align {
  display: flex;
  justify-content: flex-end;
}


.long-text-with-ellipsis {
   max-width: 100%;
   overflow: hidden;
   white-space: nowrap;
   text-overflow: ellipsis;
   display: inline-block;
}


.tag.header-id-tag {
    font-family: monospace;
    padding: 0.25rem;
    margin-right: 0.25rem;
}


.node-list {
  flex: 1;
  min-width: 0;
  margin-left: 0.5rem;
}

.separator {
  margin: 0.75rem 0;
}
</style>