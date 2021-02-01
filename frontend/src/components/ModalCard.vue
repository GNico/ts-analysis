 <template>
  <div class="modal custom-modal" :class="isActive ? 'is-active' : ''"  >
    <div class="modal-background" @click="close()"></div>
    <div class="modal-card" :style="{'min-height': minheight, 'min-width': minwidth}">
      <header class="modal-card-head">
        <p class="modal-card-title">
          {{title}}
        </p>
      </header>
      <section class="modal-card-body">
        <slot :closeHandler="close"></slot>     
      </section>
      <footer class="modal-card-foot">
        <slot name="footer-left">
          <span></span>
        </slot>
        <slot name="footer-right">
          <div>
            <button class="button is-small is-primary" @click="accept">OK</button>
            <button class="button is-small is-danger" @click="close">Cancel</button>
          </div>
        </slot>
      </footer>
    </div>
  </div>
</template>


<script>

export default {
  props: {
    isActive: {
      type: Boolean,
      required: true,
    },
    title: {
      type: String,
      default: ''
    },
    minheight: {
      type: String,
      default: '',
    },   
    minwidth: {
      type: String,
      default: '',
    },
  },
  methods: {
    accept() {
      this.$emit('accept')
    },
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


<style>

.custom-modal .modal-card {
  border: 2px solid rgba(255,255,255, 0.05);
  border-radius: 10px;
}

.custom-modal .modal-card-foot {
  justify-content: space-between;
}

.custom-modal .modal-card-title {
  font-size: 1.25rem;
}

</style>