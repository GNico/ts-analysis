<template>
<ModalCard 
  :isActive="isActive" 
  title="Save model"
  @close="close">

  <b-field horizontal label="Name">
    <b-input 
      type="text" 
      size="is-small" 
      v-model="name"
    />
  </b-field>
  <b-field horizontal label="Description">
    <b-input 
      type="textarea" 
      size="is-small" 
      v-model="description"
    />
  </b-field>

  <b-field horizontal label="Save mode">
    <div class="radio-block">
      <b-radio v-model="saveMode"
          name="saveMode"
          native-value="save">
          Save as a new model
      </b-radio>
      <b-radio v-model="saveMode"
          name="saveMode"
          native-value="update">
          Overwrite an existing model
      </b-radio>
     </div>
  </b-field>

  <b-field horizontal label="Target" v-if="saveMode == 'update'">
    <b-select size="is-small" placeholder="Select a model" v-model="modelToUpdate">
      <option
        v-for="option in allModels"
        :value="option"
        :key="option.id">
        {{ option.name }}
      </option>
    </b-select>
  </b-field>


  <template v-slot:footer-left>
    <span class="is-size-7 has-text-warning"> {{validationError}} </span>
  </template>
  <template v-slot:footer-right>
    <div>
      <button class="button is-small is-primary" @click="performSave">Save</button>
      <button class="button is-small" @click="close">Cancel</button>
    </div>
  </template>
</ModalCard>
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
    close() {
      this.$emit('close')
    },
    performSave() {
      this.saveMode == 'save' ? this.save() : this.update()
    },
    update() {
      this.$emit('update', {id: this.modelToUpdate.id, name: this.name, description: this.description})
    },
    save() {
      this.$emit('save', {name: this.name, description: this.description})
    }

  }
}


</script>


<style>
  
.radio-block {
   line-height: 2;
}


</style>