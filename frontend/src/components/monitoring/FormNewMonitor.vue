<template>
<form @submit.prevent="handleSubmit">
  <div class="modal-card" style="width: 300px; border-radius: 0.4em">
    <section class="modal-card-body">
      <b-field label="Name">
        <b-input v-model="form.name" required/>
      </b-field>              
    </section>
    <footer class="modal-card-foot">
      <button class="button is-primary" :disabled="loading">Create</button>  
      <div v-if="loading">
        <i class="mdi mdi-loading icn-spinner"></i> Processing
      </div>
    </footer>
  </div>
</form>
</template>

<script>
export default {
  props: {
    loading: {
      type: Boolean,
      default: true
    }
  },
  data() {
    return {
      form: {
        name: '',
      },
    }
  },
  methods: {
    clear() {
      this.form.name = ''
    },
    handleSubmit() {
      this.$emit('submit', this.form)
    },  
  }
}

</script>