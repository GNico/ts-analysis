<template>
<form @submit.prevent="handleSubmit">
  <div class="modal-card" style="width: 300px; border-radius: 0.4em">
    <section class="modal-card-body">
      <b-field label="Name">
        <b-input v-model="form.name" size="is-small" required/>
      </b-field>    
      <div class="has-text-right">
        <button class="button is-primary mt-2" :disabled="loading">
          {{buttonText}} <i v-if="loading" class="mdi mdi-loading icn-spinner"></i>
        </button>   
      </div>   
    </section>
  </div>
</form>
</template>

<script>
export default {
  props: {
    loading: {
      type: Boolean,
      default: false
    },
    buttonText: {
      type: String,
      default: 'Create'
    },   
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