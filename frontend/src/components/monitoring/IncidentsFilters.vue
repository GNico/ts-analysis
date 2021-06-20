<template>
<b-dropdown
  ref="dropdown"
  :position="position"
  append-to-body
  trap-focus
  @active-change="active = $event">
  <template #trigger>
    <a class="button is-info is-small" :class="{ 'is-outlined': !active }">
      <span class="icon"><i class="mdi mdi-filter-variant"></i></span>
      <span>Filters</span>
      <span class="icon"><i class="mdi mdi-menu-down"></i></span>
    </a>
  </template>

  <b-dropdown-item
    aria-role="menu-item"
    :focusable="false"
    custom
    paddingless>
    <div class="modal-card" style="max-width:400px; border-radius: 0.4em">    
      <section class="modal-card-body">
        <b-field horizontal label="Client">
          <b-input 
            v-model="filters.client"            
            type="text" 
            size="is-small" 
            expanded
            icon-right="close-circle"
            icon-right-clickable
            @icon-right-click="client = ''"/>
        </b-field>

        <b-field horizontal label="Monitor">
          <b-input 
            v-model="filters.monitor"
            type="text" 
            size="is-small" 
            expanded
            icon-right="close-circle"
            icon-right-clickable
            @icon-right-click="monitor = ''"/>
        </b-field> 

        <b-field horizontal label="Detector">
          <b-input 
            v-model="filters.detector"
            type="text" 
            size="is-small" 
            expanded
            icon-right="close-circle"
            icon-right-clickable
            @icon-right-click="detector = ''"/>
        </b-field> 

        <b-field horizontal label="State">
          <b-select v-model="filters.state" size="is-small" >
            <option value="">All</option>
            <option value="Open">Open</option>
            <option value="Closed">Closed</option>
          </b-select>
        </b-field>

        <b-field class="has-text-right sticky-container">
            <a class="button is-primary has-text-weight-semibold" @click="apply">
              Apply
            </a>
        </b-field> 
          
      </section>
    </div>
  </b-dropdown-item>
</b-dropdown>
</template>


<script>

export default {
  props: {
    position: {
      type: String,
      default: "is-bottom-right"
    },   
  },
  data() {
    return {
      active: false,
      filters: {
        client: '',
        monitor: '',
        detector: '',
        state: '',
      }
    }
  },
  methods: {
    apply() {
      this.$emit("apply", this.filters)
      this.$refs.dropdown.toggle()
    }
  }
}
</script>