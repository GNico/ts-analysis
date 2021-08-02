<template>
<form ref="theform" @submit.prevent>

<ModalCard 
  :isActive="isActive" 
  title="Save analysis"
  @close="close">

  <b-field horizontal label="Name">
    <b-input 
      type="text" 
      size="is-small" 
      v-model="name"
      required
    />
  </b-field>
  <b-field horizontal label="Description">
    <b-input 
      type="textarea" 
      size="is-small" 
      v-model="description"
    />
  </b-field>

  <template v-slot:footer-right>
    <div>
      <button class="button is-small is-primary" @click="save">Save</button>
      <button class="button is-small is-primary" @click="saveAs" :disabled="!isSaveAsAllowed">Save as</button>
      <button class="button is-small" @click="close">Cancel</button>
    </div>
  </template>
</ModalCard>

</form>
</template>


<script>
import ModalCard from "../ModalCard"

export default {
  components: { ModalCard },
  props: { 
    isActive: {
      type: Boolean,
      default: false
    },
    analysis: {
      type: Object,
      default: () => {return {} }
    },
  },
  data() {
    return {
      name: this.analysis.name,
      description: this.analysis.description,
    }
  },
  computed: {
    hasSaveId() {
      return !!this.analysis.saveId
    },
    isSaveAsAllowed() {
      return (this.hasSaveId && this.analysis.name != this.name) 
    },
  },
  methods: {
    close() {
      this.$emit('close')
    },
    save() {
      if (!this.checkValidation()) return
      if (this.hasSaveId) {
        this.$emit('update', {name: this.name, description: this.description})
      } else {
        this.saveAs()
      }
      this.close()
    },  
    saveAs() {
      if (!this.checkValidation()) return
      this.$emit('save', {name: this.name, description: this.description})
      this.close()
    },
    checkValidation() {
      return this.$refs.theform.checkValidity()  
    },
  },
  watch: {
    analysis(newVal) { 
      this.name = newVal.name
      this.description = newVal.description
    }
  }
}
</script>


<style>
.radio-block {
   margin-bottom: 1rem;
}
</style>