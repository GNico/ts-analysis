<template>
<div v-show="options.active !== undefined">
  <b-field label="Monitoring">
     <b-switch v-model="options.active" size="is-small" type="is-primary" passive-type="is-grey">{{options.active ? 'Active' : 'Disabled'}}</b-switch>
  </b-field>

  <b-field label="Time interval">
    <b-input 
      class="shortest-field"
      v-model="options.time_interval"
      type="text" 
      pattern="^[0-9]+[mhd]$" 
      size="is-small" />
  </b-field>

  <b-field label="Alerts">
     <b-switch v-model="options.alerts_enabled" size="is-small" type="is-primary">{{options.alerts_enabled ? 'Enabled' : 'Disabled'}}</b-switch>
  </b-field>

  <b-field>
    <a class="button is-primary is-medium has-text-weight-semibold" @click="updateOpts">
      Update
    </a>    
  </b-field> 
</div>
</template>



<script>
export default {
  props: {
    details: {
      type: Object,
      default: () => {return {}}
    }
  },
  data() {
    return {
      options: {
        active: undefined,
        alerts_enabled: undefined,
        time_interval: undefined
      }
    }
  },
  methods: {
    updateOpts() {
      this.$emit('update', this.options)
    }
  },
  watch: {
    details: {
      immediate: true,
      deep: true,
      handler(newOpts) {
        Object.keys(this.options).forEach(key => {
          if (this.options.hasOwnProperty(key) && this.options[key] !== this.details[key]) {
            this.options[key] = this.details[key] 
          }
        })
      }
    }
  }
}
</script>



