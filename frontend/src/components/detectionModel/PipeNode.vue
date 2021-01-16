<template>
<b-collapse
  class="card"
  animation="slide"
  :open="false">
  <template #trigger="props">
    <div class="card-header">
      <div class="card-header-title">
        <p> {{title}} </p>        
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
      <div class="field is-horizontal">
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
                Source node
                <b-icon size="is-small" icon="menu-down"/>
              </b-tag>
            </template>

            <b-dropdown-item value='none' v-if="!allowMultiple">
              <span> None </span>
            </b-dropdown-item>
            <b-dropdown-item v-for="item in sourceNodesList" :key="item.id" :value="item" aria-role="listitem">
              <span>{{item.title}} (ID: {{item.id}})</span>
            </b-dropdown-item>
          </b-dropdown>
        </div>

        <!--Display selected source nodes -->
        <div class="field-body">
          <div class="field is-grouped is-grouped-multiline">
            <div v-if="!sourceNodes.length"><i>None</i></div>
            <div v-else class="control" v-for="node in sourceNodes">
              <div class="tags has-addons">
                <a class="tag is-info" size="is-small">ID</a>
                <a class="tag is-dark" size="is-small" style="font-family: monospace">{{node.id}}</a>
              </div>
            </div>      
          </div> 
        </div>
      </div>

      <!--Parameters list -->
      <b-field v-for="item in paramsComponents" :key="item.name" horizontal :label="item.name">
        <component
          :is="item.component.name"
          v-bind="item.component.props"
          :value="paramsData[item.name]"
          @input="paramsDataChange(item.name, $event)"/>
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
    title: {
      type: String,
      default: 'Unknown'
    },
    desc: {
      type: String,
      default: 'Unknown'
    },
    type: {
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
    }
  },
  computed: {
    paramsComponents() {
      let components = []
      this.params.forEach(elem => {
        components.push({
          name: elem.name,
          component: this.getFieldComponent(elem.type),
        })
      })
      return components
    },
    sourceNodesList() {
      let id = this.id
      if (this.type === 'detector' ||  this.type === 'transformer')
        return this.nodes.filter(elem => elem.id !== this.id && elem.type === 'transformer')
      if (this.type === 'aggregator') {
        return this.nodes.filter(elem => elem.id !== this.id && (elem.type === 'detector' || elem.type === 'aggregator'))
      }
    },
    allowMultiple() {
      return this.type === 'aggregator'
    }

  },
  methods: {
    getFieldComponent(type) {
      switch (type) {
        case 'number': 
          return {
            name: 'b-input',
            props: {
              type: 'number',
              step: 0.1,
              size: 'is-small',
            }
          }
        case 'boolean':
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
      this.$emit('nodeParamsChange', {id: this.id, [name]: event})
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
    }
  }
}
</script>

<style>

</style>