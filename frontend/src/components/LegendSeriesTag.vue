<template>
<div class="tags has-addons" 
@mouseover="hover = true"
@mouseleave="hover = false">
  
  
  <span class="tag has-text-weight-bold is-family-monospace" :class="!hidden ? 'active-legend' : ''">  
    <span class="legend-line" :style="{color: lineColor()}"> — </span> 
    <slot></slot>
  </span>
  <template v-if="hover">
    <b-tooltip :label="hidden ? 'Show' : 'Hide'" size="is-small" type="is-dark">
      <a class="tag" @click="toggleVisibiity"><b-icon icon="eye" size="is-small"></b-icon></a>
    </b-tooltip>
    <b-tooltip label="Settings" size="is-small" type="is-dark">
      <a class="tag" @click="openSettings"><b-icon icon="cog" size="is-small"></b-icon></a>
    </b-tooltip>
    <b-tooltip label="Delete" size="is-small" type="is-dark">
      <a class="tag" @click="remove"><b-icon icon="close-thick" size="is-small"></b-icon></a>
    </b-tooltip>
  </template>
</div>
</template>


<script>

export default {
  props: {
    color: String,
    id: String,
  },
  data() {
    return {
      hover: false,
      hidden: false,
    }
  },
  methods: {
    toggleVisibiity() {
      this.hidden = !this.hidden
      this.$emit('show', {id: this.id, hidden: this.hidden})
    },
    openSettings() {
      this.$emit('settings', this.id)
    },
    remove() {
      this.$emit('delete', this.id)
    },
    lineColor() {
      if (!this.color) {
        return 'transparent'
      } else if (this.hidden) {
        return ''
      } else {
        return this.color
      }
    }

  }
}

</script>



<style scoped>

a:hover {
  text-decoration: none;
}

.active-legend {
  color: white;
}

.legend-line {
  font-size: 1.5rem;
  margin-right: 0.25rem;
}

</style>