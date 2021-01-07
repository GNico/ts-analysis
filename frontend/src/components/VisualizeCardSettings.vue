<template>

<ModalCard 
  :isActive="isActive" 
  title="Chart settings"
  @close="close"
  @accept="updateSettings">

  <div class="columns is-multiline is-marginless is-gapless is-paddingless">

    <div class="column is-full"> 
      <div class="field is-horizontal">
        <div class="field-label is-small has-text-left">
          <label class="label">Background</label>
        </div>
        <div class="field-body">
          <div class="field is-narrow short-field">
            <div class="control">
              <ColorSelect v-model="chartSettings.backgroundColor"/>
            </div>
          </div>
        </div>
      </div>

      
      <div class="field is-horizontal">
        <div class="field-label is-small has-text-left">
          <label class="label">Line width</label>
        </div>
        <div class="field-body">
          <div class="field is-narrow shorter-field">
            <div class="control">
              <input class="input is-small" type="number" min="1" v-model.number="chartSettings.lineWidth">
            </div>
          </div>
        </div>
      </div>

      <div class="field is-horizontal">
        <div class="field-label is-small has-text-left">
          <label class="label">Margin left</label>
        </div>
        <div class="field-body">
          <div class="field is-narrow shorter-field">
            <div class="control">
              <input class="input is-small" type="number" min="0" v-model.number="chartSettings.marginLeft">
            </div>
          </div>
        </div>
      </div>

       <div class="field is-horizontal">
        <div class="field-label is-small has-text-left">
          <label class="label">Margin top</label>
        </div>
        <div class="field-body">
          <div class="field is-narrow shorter-field">
            <div class="control">
              <input class="input is-small" type="number" min="0" v-model.number="chartSettings.marginTop">
            </div>
          </div>
        </div>
      </div>

       <div class="field is-horizontal">
        <div class="field-label is-small has-text-left">
          <label class="label">Margin bottom</label>
        </div>
        <div class="field-body">
          <div class="field is-narrow shorter-field">
            <div class="control">
              <input class="input is-small" type="number" min="0" v-model.number="chartSettings.marginBottom">
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

</ModalCard>
</template>



<script>
import ModalCard from './ModalCard';
import ColorSelect from './inputs/ColorSelect';  

export default {
  components: { ModalCard, ColorSelect  },
  props: {
    isActive: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      chartSettings: {
        backgroundColor: '',
        marginLeft: 50,
        marginTop: 50,
        marginBottom: 50,
        lineWidth: 5,
      }
    }
  },
  computed: {
    savedSettings() {
      return this.$store.state.visualize.settings
    }
  },
  methods: {
    close() {
      this.$emit('close')
    },
    updateSettings(options) {
      this.$store.dispatch('visualize/changeSettings', this.chartSettings)
      this.close()
    },
  },
  watch: {
    savedSettings: {
      immediate: true,
      handler: function (newSettings) {
        if (newSettings) {
          for (const key of Object.keys(newSettings)) {
            if (this.chartSettings.hasOwnProperty(key)) { 
                this.chartSettings[key] = newSettings[key]
            }
          }
        }
      }
    }
  }
}

</script>


<style scoped>

.color-input {
  visibility: hidden;
}

.color-box {
  max-width: 30%;
}

</style>