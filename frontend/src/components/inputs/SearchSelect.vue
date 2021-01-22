<template>
  <b-autocomplete
    :value="value"
    @input="$emit('input', $event)"
    :placeholder="placeholder"
    open-on-focus
    :size="size"
    :data="reducedDataList"
    @select="emitSelected"
    ref=autocomplete 
    @keydown.native.enter="$event.target.blur(); closeOptions()"
    @blur="onBlur"> 
      <template slot="empty">No results</template>
  </b-autocomplete>  
</template>


<script>
export default {
  props: {
    value: {
      default: '',
    },
    data: {
      required: false
    },
    size: {
      required: false,
      default: "is-small"
    },
    maxOptionsDisplayed: {
      type: Number,
      default: 50
    },
    placeholder: {
      default: ""
    },
    clearOnBlur: {
      type: Boolean,
      default: true
    }
  },
  data() {
    return {}
  },
  computed: {
    filteredDataList() {
      return  this.data.filter(
        (item) => {return item.toLowerCase().match(this.value.toLowerCase())} )
    },
    reducedDataList() {
      return this.filteredDataList.slice(0, this.maxOptionsDisplayed)
    },
  },
  methods: {
    onBlur() {
      if (this.clearOnBlur && this.filteredDataList.length === 0) {
        this.$emit('input', '')
      } 
    },
    closeOptions() {            
      this.$refs.autocomplete.isActive = false
    },
    emitSelected(option) {
      this.$emit('selected', option)
    },
    clear() {
      this.inputValue = ''
    }
  },
}
</script>