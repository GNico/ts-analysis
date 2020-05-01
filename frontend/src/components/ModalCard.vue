 <template>
  <div class="modal" :class="isActive ? 'is-active' : ''"  >
    <div class="modal-background" @click="close()"></div>
    <div class="modal-card">
      <slot :closeHandler="close"></slot>     
    </div>
  </div>
 </template>


<script>

export default {
  props: {
    isActive: {
      type: Boolean,
      required: true,
    }
  },
  methods: {
    close() {
      this.$emit('close')
    },
    keyPress({ key }) {
      if (this.isActive && (key === 'Escape' || key === 'Esc')) {
        this.close()
      }
    },
  },
  created() {
    if (typeof window !== 'undefined') {
      document.addEventListener('keyup', this.keyPress)
    }
  },
  beforeDestroy() {
    if (typeof window !== 'undefined') {
      document.removeEventListener('keyup', this.keyPress)
    }
  }

}

</script>


<style scoped>

.modal-card {
  max-height: 70%;
}

</style>