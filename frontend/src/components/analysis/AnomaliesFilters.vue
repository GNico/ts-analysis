<template>
<b-dropdown
  :position="position"
  append-to-body
  trap-focus
  @active-change="active = $event">
  <template #trigger>
    <a class="button is-info is-small" :class="{ 'is-outlined': !active }">
      <span class="icon"><i class="mdi mdi-filter-variant"></i></span>
      <span>Filters</span>
      <span class="icon"><i class="mdi mdi-menu-down"></i></span>
    </a>
  </template>

  <b-dropdown-item
    aria-role="menu-item"
    :focusable="false"
    custom
    paddingless>
    <div class="modal-card" style="max-width:400px; border-radius: 0.4em">    
      <section class="modal-card-body">
        <b-field horizontal label="Min Duration">
          <b-tooltip
            label="Input must be a number followed by a valid letter [ m = minutes, h = hour, d = day ]"
            size="is-large"
            position="is-bottom"
            multilined>
            <b-input 
              :value="minDuration" 
              @input="updateMinDuration" 
              ref="regexinput" 
              type="text" 
              pattern="^[0-9]+[mhd]$" 
              size="is-small" 
              expanded
              icon-right="close-circle"
              icon-right-clickable
              @icon-right-click="updateMinDuration('')"/>
            </b-tooltip> 
          </b-field> 

          <b-field horizontal label="Score threshold" >
            <b-slider :value="scoreThreshold" @input="update('scoreThreshold', $event)" lazy></b-slider>
          </b-field>

          <b-field horizontal label="">
            <b-checkbox :value="showSeries" @input="update('showSeries', $event)">
              <strong class="has-text-white">Show series</strong>
            </b-checkbox>        
          </b-field>
              
          <b-field horizontal label="">
            <b-checkbox :value="showMinMax" @input="update('showMinMax', $event)">
              <strong class="has-text-white">Show min and max values</strong>
            </b-checkbox>        
          </b-field>

          <b-field horizontal label="">
            <b-checkbox :value="showTrend" @input="update('showTrend', $event)">
              <strong class="has-text-white">Show trend</strong>
            </b-checkbox>        
          </b-field>
        </section>
      </div>
    </div>
  </b-dropdown-item>
</b-dropdown>
</template>


<script>

export default {
  props: {
    position: {
      type: String,
      default: "is-bottom-left"
    },
    minDuration: {
      type: String,
      default: '',
    },
    minDurationTime: {
      type: Number,
      default: 0
    },
    scoreThreshold: {
      type: Number,
      default: 0,
    },
    showSeries: {
      type: Boolean,
      default: true,
    },
    showMinMax: {
      type: Boolean,
      default: true,
    },
    showTrend: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      active: false,
    }
  },
  methods: {
    updateMinDuration(value) {
      let minDurationTime = 0
      if (value && this.$refs.regexinput.checkHtml5Validity()) {
        let numbers = value.match(/\d+/g)
        let letter = value.match(/[mhd]/g)
        let ms = 0
        switch (letter[0]) {
          case "m":
            ms = 60000
            break
          case "h":
            ms = 3600000
            break
          case "d": 
            ms = 86400000
            break
          default:
            break
          }
        minDurationTime = parseInt(numbers[0]) *  ms 
      }
      this.$emit('update', {minDuration: value, minDurationTime: minDurationTime})
    },    
    update(key, value) {
      this.$emit('update', {[key]: value} )
    }
  }
}
</script>
