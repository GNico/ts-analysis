<template>
<form ref="theform" @submit.prevent>

<ModalCard 
  :isActive="isActive" 
  title="Save template model"
  @close="close">

    <b-field horizontal label="Save options">
      <div class="radio-block">
        <b-radio v-model="saveMode"
            name="saveMode"
            native-value="save">
            Save as new template model
        </b-radio>
        <b-radio v-model="saveMode"
            name="saveMode"
            native-value="update">
            Update existing template model
        </b-radio>
       </div>
    </b-field>

    <b-field horizontal label="Template to update" v-if="saveMode == 'update'">
      <b-select size="is-small" placeholder="Select existing template" v-model="modelToUpdate" required @input="populateFields">
        <option
          v-for="option in allModels"
          :value="option"
          :key="option.id">
          {{ option.name }}
        </option>
      </b-select>
    </b-field>


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

  

    <template v-slot:footer-left>
      <span class="is-size-7 has-text-warning"> {{validationError}} </span>
    </template>
    <template v-slot:footer-right>
      <div>
        <button class="button is-small is-primary" @click="checkValidation">Save</button>
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
      default: false,
    },
    allModels: {
      type: Array,
      default: () => []
    },
  },
  data() {
    return {
      name: '',
      description: '',
      saveMode: 'save',
      modelToUpdate: undefined,
    }
  },
  computed: {
    validationError() {
      return ''
    }
  },
  methods: {
    resetState() {
      this.saveMode = 'save'
      this.name = ''
      this.description = ''
      this.modelToUpdate = undefined
    },
    close() {
      this.$emit('close')
      this.resetState()
    },
    performSave() {
      this.saveMode == 'save' ? this.save() : this.update()
      this.resetState()
    },
    update() {
      this.$emit('update', {id: this.modelToUpdate.id, name: this.name, description: this.description})
    },
    save() {
      this.$emit('save', {name: this.name, description: this.description})
    },
    checkValidation() {
      if (this.$refs.theform.checkValidity()) {
        this.performSave()
      }
    },
    populateFields(event) {
      this.name = event.name
      this.description = event.description
    }
  }
}
</script>


<style>
.radio-block {
   margin-bottom: 1rem;
}
</style>