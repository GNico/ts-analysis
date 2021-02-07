<template>

<ModalCard 
  :isActive="isActive" 
  title="Save Analysis"
  minheight="50%"
  @close="close">

  A persisted analysis was loaded in this view.
  Do you wish to save its changes or save as new instance?

  <template v-slot:footer-right>
    <div>
      <button class="button is-small is-primary" @click="update">Overwrite</button>
      <button class="button is-small is-primary" @click="save">New Save</button>
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
    }
  },
  data() {
    return {
    }
  },
  methods: {
    close() {
      this.$emit('close')
    },
    update() {
      this.$emit('update')
    },
    save() {
      this.$emit('save')
    }
  }
}


</script>



