<template>

  <label class="label is-small color-box " :style="{'background-color': color}">
    <input class="input is-small color-input" type="color" :value="color" @change="colorSelected"> 
  </label>   
     
</div>
</template>


<script>

export default {
  props: {
    value: { 
      type: String,
      default: '#ff0000',
    },
  },
  data () {
    return {
      color: this.value,
    }
  },
  methods: {
    colorSelected (event) {
      this.color = event.target.value
      this.$emit('input', this.color)
    }
  },
  watch: {
    value(newVal) {
      this.color = newVal
    }
  }
}
    

</script>


<style scoped>

.color-box {
  box-shadow: none;
  border-radius: 3px;
  border-width: 2px;
}

.color-input {
  visibility: hidden;
}

</style>