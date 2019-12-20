<template>

<span>
 test  {{ name }} and {{ client.details }}
</span>

</template>



<script>
export default {
  props: {
    name: {
      default: '',
      type: String,
    }
  }, 
  data() {
    return {      
    }
  },
  computed: {
    client() {
      return this.$store.state.clients.details
    }
  },
  watch: { 
    name: function(newVal, oldVal) { 
      this.$store.dispatch('clients/fetchClientDetails', newVal)          
    }
  }
}

</script>