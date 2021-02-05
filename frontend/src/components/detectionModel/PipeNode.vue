<template>
  <b-collapse
    class="card"
    animation="slide"
    :open="false">
    <template #trigger="props">
      <div class="card-header" @mouseover="showDelete = true" @mouseleave="showDelete = false">
        <div class="card-header-title">
          <b-tag 
            size="is-medium"
            :closable="showDelete"
            closeType='is-warning'
            aria-close-label="Close tag"
            @close="deleteNode">
            {{display}}
          </b-tag>         
        </div>
        <a class="card-header-icon">
          <div class="tags has-addons">
            <a class="tag is-info" size="is-small">ID</a>
            <a class="tag is-dark" size="is-small" style="font-family: monospace">{{id}}</a>
            <b-icon :icon="props.open ? 'menu-up' : 'menu-down'"/>
          </div>
        </a>
      </div>
    </template>
    <div class="card-content">
      <div class="content">

        <!--Source node selection-->
        <div class="field is-horizontal node-fields">
          <div class="field-label">
            <b-dropdown
              :value="sourceNodes"
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
              <b-dropdown-item v-for="item in sourceNodesList" :key="item.id" :value="item" aria-role="listitem">
                <span>{{item.type}} (ID: {{item.id}})</span>
              </b-dropdown-item>
            </b-dropdown>
          </div>

          <!--Display selected source nodes -->
          <div class="field-body">
            <div class="field is-grouped is-grouped-multiline">
              <div v-if="!sourceNodes.length"><i>None</i></div>
              <div v-else class="control" v-for="node in sourceNodes">
                <div class="tags has-addons">
                  <span class="tag is-info" size="is-small">ID</span>
                  <span class="tag is-dark" size="is-small" style="font-family: monospace">{{node.id}}</span>
                </div>
              </div>      
            </div> 
          </div>
        </div>

        <!--Parameters list -->
        <b-field v-for="item in paramsComponents" :key="item.id" horizontal class="node-fields">
          <template #label>
            {{item.display}}
            <b-tooltip type="is-info" :label="item.desc">
              <b-icon size="is-small" icon="help-circle-outline"></b-icon>
            </b-tooltip>
          </template>
          <component
            :is="item.component.name"
            v-bind="item.component.props"
            :value="paramsData[item.id]"
            @input="paramsDataChange(item.id, $event)"/>
        </b-field>
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
    type: {
      type: String,
      default: 'Unknown'
    },
    display: {
      type: String,
      default: 'Unknown'
    },
    desc: {
      type: String,
      default: 'Unknown'
    },
    group: {
      type: String,
      default: 'Unknown'
    },
    params: {
      type: Array,
      default: () => []
    },
    paramsData: {
      type: Object,
      default: () => {return {}} 
    },
    nodes: {
      type: Array,
      default: () => []
    },
    sourceNodes: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      showDelete: false,
    }
  },
  computed: {
    paramsComponents() {
      let components = []
      this.params.forEach(elem => {
        components.push({
          id: elem.id,
          display: elem.display,
          desc: elem.desc,
          component: this.getFieldComponent(elem.type),
        })
      })
      return components
    },
    sourceNodesList() {
      let id = this.id
      if (this.group === 'detector' ||  this.group === 'transformer')
        return this.nodes.filter(elem => elem.id !== this.id && elem.group === 'transformer')
      if (this.group === 'aggregator') {
        return this.nodes.filter(elem => elem.id !== this.id && (elem.group === 'detector' || elem.group === 'aggregator'))
      }
    },
    allowMultiple() {
      return this.group === 'aggregator'
    }

  },
  methods: {
    getFieldComponent(type) {
      switch (type) {
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
              max: 1,
              min: 0,
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
      this.$emit('nodeSourceChange', {id: this.id, sourceNodes: sourceNodes} )
    },
    deleteNode() {
      this.$emit('nodeDelete', this.id)
    }
  }
}
</script>



<style>

.node-fields .field-label {
    flex-grow: 5;
}

</style>