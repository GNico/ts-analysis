<template>
<form ref="theform" @submit.prevent>
  <ModalCard 
    :isActive="isActive" 
    :title="title"
    @close="close">

    <b-field horizontal label="Name">
      <b-input 
        v-model="options.name"
        type="text" 
        size="is-small" 
        required
      />
    </b-field>
    <b-field horizontal label="Time zone">
      <b-select 
        v-model="options.utc_offset"
        size="is-small">
        <option
          v-for="offset in UTCOffsets"
          :value="offset[1]"
          :key="offset[1]">
          {{ offset[0] }}
        </option>
      </b-select>
    </b-field>

    <b-field class="mt-4" horizontal label="">
      <b-checkbox v-model="deleteOld" >
        <strong class="has-text-white">Automatically delete old data</strong>
      </b-checkbox>        
    </b-field>

    <b-field v-if="deleteOld" horizontal label="Delete older than">            
      <b-input type="number" size="is-small" step="1" min="1" :value="periodNum"></b-input>
      <b-select size="is-small" :value="periodUnit">
          <option value="m">minutes</option>
          <option value="d">days</option>
          <option value="y">years</option>
      </b-select>            
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
import { timezones } from "@/utils/datetimeConstants"

export default {
  components: { ModalCard },
  props: { 
    isActive: {
      type: Boolean,
      default: false,
    },
    settings: {
      type: Object,
      default: () => {}
    },
  },
  data() {
    return {
      options: {
        name: '',
        utc_offset: '',
      },
      //the following is not implemented, just a placeholder for show
      deleteOld: false,     
      periodNum: 2,
      periodUnit: "y", 
    }
  },
  computed: {
    title() {
      return 'Client settings: ' + this.settings.name
    },
    validationError() {
      return ''
    },
    UTCOffsets() {
      return timezones.UTCOffsets
    }
  },
  methods: {
    close() {
      this.$emit('close')
    },
    update() {
      this.$emit('update', {name: this.settings.name, options: this.options})
      this.close()
    },
    checkValidation() {
      if (this.$refs.theform.checkValidity()) {
        this.update()
      }
    },

  },
  watch: {
    settings: {
      immediate: true,
      handler() {
        Object.keys(this.options).forEach(key => {
          this.options[key] = this.settings[key]
        })
      }
    }
  }
}
</script>


<style>

</style>