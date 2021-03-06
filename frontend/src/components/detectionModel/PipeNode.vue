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
            {{nodeDefiniton.display}}
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
              :value="nodeData.sourceNodes"
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
          </div>
          <!--Display selected source nodes -->
          <div class="field-body">
            <div class="field is-grouped is-grouped-multiline">
              <div v-if="!nodeData.sourceNodes.length"><i>None</i></div>
              <div v-else class="control" v-for="nodeid in nodeData.sourceNodes">
                <div class="tags has-addons">
                  <span class="tag is-info" size="is-small">ID</span>
                  <span class="tag is-dark" size="is-small" style="font-family: monospace">{{nodeid}} : {{getNode(nodeid).type}}</span>
                </div>
              </div>      
            </div> 
          </div>
        </div>
        <!--Parameters list -->
        <b-field v-for="param in paramsComponents" :key="param.id" horizontal class="node-fields">
          <template #label>
            {{param.display}}
            <b-tooltip type="is-info" :label="param.desc">
              <b-icon size="is-small" icon="help-circle-outline"></b-icon>
            </b-tooltip>
          </template>
          <component
            :is="param.component.name"
            v-bind="param.component.props"
            :value="nodeData.paramsData[param.id]"
            @input="paramsDataChange(param.id, $event)"/>
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
    nodes: {
      type: Array,
      default: () => []
    },
    nodeDefiniton: {
      type: Object,
      default: () => {return {
        type: '',
        desc: '',
        display: '',
        params: '',

      }}
    }
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
    },
    getNode(id) {
      return this.nodes.find(item => item.id === id)
    }
  }
}
</script>



<style>

.node-fields .field-label {
    flex-grow: 5;
}

</style>