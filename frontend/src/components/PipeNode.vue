<template>

<b-collapse
  class="card"
  animation="slide"
  :open="false">
  <template #trigger="props">
    <div class="card-header">
      <p class="card-header-title">{{title}}</p>
      <a class="card-header-icon">
        <b-icon :icon="props.open ? 'menu-up' : 'menu-down'"/>
      </a>
    </div>
  </template>
  <div class="card-content">
    <div class="content">

      <!--Edge selection-->
      <div class="field is-horizontal">
        <div class="field-label">
          <b-dropdown
            :value="inputNodesSelected"
            @change="inputNodesChange"
            multiple
            aria-role="list">
            <template #trigger>
              <b-tag
                  type="is-info"     
                  size="is-small"             
                  icon-right="menu-down">
                  Node input
              </b-tag>
            </template>

            <b-dropdown-item v-for="item in inputNodes" :value="item" aria-role="listitem">
                <span>{{item}}</span>
            </b-dropdown-item>
          </b-dropdown>
        </div>

        <!--Display selected edges -->
        <div class="field-body">
          <div class="field is-grouped is-grouped-multiline">
            <div class="control" v-for="node in inputNodesSelected">
              <div class="tags has-addons">
                <a class="tag is-info" size="is-small">ID</a>
                <a class="tag is-dark" size="is-small">{{node}}</a>
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
    inputNodes: {
      type: Array,
      default: () => []
    },
    paramsData: {
      type: Object,
      default: () => {return {}} 
    },
    inputNodesSelected: {
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
    inputNodesChange(event) {
      this.$emit('nodeInputChange', {id: this.id, inputNodes: event} )
    }
  }
}

</script>

<style>

</style>