<template>
<b-dropdown
  :position="position"
  append-to-body
  trap-focus
  @active-change="active = $event">
  <template #trigger>
    <a class="button is-info is-small" :class="{ 'is-outlined': !active }">
      <span class="icon"><i class="mdi mdi-cog"></i></span>
      <span>Options</span>
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
        <b-field horizontal label="Axis interval">
          <b-select :value="axisInterval" @input="update('axisInterval', $event)" size="is-small">
            <option value="">auto</option>
            <option value="month">month</option>
            <option value="week">week</option>
            <option value="day">day</option>
            <option value="hour">hour</option>
          </b-select>
        </b-field>        
        <b-field horizontal label="">
          <b-checkbox :value="showSeries" @input="update('showSeries', $event)">
            <strong class="has-text-white">Show series</strong>
          </b-checkbox>        
        </b-field>
            
        <b-field horizontal label="">
          <b-checkbox :value="showMinMax" @input="update('showMinMax', $event)">
            <strong class="has-text-white">Show min and max values</strong>
          </b-checkbox>        
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
      default: "is-bottom-left"
    },    
    showSeries: {
      type: Boolean,
      default: true,
    },
    showMinMax: {
      type: Boolean,
      default: true,
    },
    axisInterval: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      active: false,
    }
  },
  methods: {   
    update(key, value) {
      this.$emit('update', {[key]: value} )
    }
  }
}
</script>
