<template>
<div class="date-range-bar" >

    <div class="date-range-bar__buttons">
      <div class="label is-marginless"> Range: </div>
      <div class="button is-info is-small" :class="{ 'is-outlined': activeBtn !== 'btn1' }" @click="setActive('btn1'); setAll()" >
        All
      </div>       
      <div class="button is-info is-small" :class="{ 'is-outlined': activeBtn !==  'btn2' }" @click="setActive('btn2'); setLast(365)" >
        Last year
      </div>
      <div class="button is-info is-small" :class="{ 'is-outlined': activeBtn !==  'btn3' }" @click="setActive('btn3'); setLast(30)" >
        Last month
      </div>
      <div class="button is-info is-small" :class="{ 'is-outlined': activeBtn !==  'btn4' }" @click="setActive('btn4'); setLast(7)" >
        Last week
      </div> 
      <div class="button is-info is-small" :class="{ 'is-outlined': activeBtn !==  'btn5' }" @click="setActive('btn5'); setLast(1)" >
        Last day
      </div>
    </div>        

    <div class="date-range-bar__inputs">
      <div class="datepicker-field">
        <label class="label">From</label>
        <b-datepicker 
            v-model="selectedRange.start"
            icon-pack="fas"
            :first-day-of-week="1"
            placeholder="Click para seleccionar..."
            size="is-small"
            @input="deactivateButton">

            <button class="button is-primary"
                @click="selectedRange.start = new Date()">
                <b-icon pack="fas" icon="calendar-day"></b-icon>
                <span>Today</span>
            </button>

            <button class="button is-danger"
                @click="selectedRange.start = null">
                <b-icon pack="fas" icon="times"></b-icon>
                <span>Clear</span>
            </button>
        </b-datepicker>
      </div>

      <div class="datepicker-field">
        <label class="label">To</label>
        <b-datepicker 
            v-model="selectedRange.end"
            icon-pack="fas"
            :first-day-of-week="1"
            placeholder="Click para seleccionar..."
            size="is-small"
            @input="deactivateButton">

            <button class="button is-primary"
                @click="selectedRange.end = new Date()">
                <b-icon pack="fas" icon="calendar-day"></b-icon>
                <span>Today</span>
            </button>

            <button class="button is-danger"
                @click="selectedRange.end = null">
                <b-icon pack="fas" icon="times"></b-icon>
                <span>Clear</span>
            </button>
        </b-datepicker>

      </div>

      <div>
        <button class="button is-primary is-small" @click="update">
          Update
        </button> 
      </div>  
    </div>                
</div>

</template>


<script>

export default {
  props: {
    range: {
      type: Object,
    },
  },
  data () {
    return {
      selectedRange: {
        start: this.range.start,
        end: this.range.end,
      },
      activeBtn: null,
      buttonIsActive: false,
    }
  },
  methods: {
    update() {
      this.$emit('input', { start: this.selectedRange.start, end: this.selectedRange.end })
    },
    setAll() {
      this.selectedRange.start = null
      this.selectedRange.end = null
      this.update()
    },
    setLast(days) {
      let pastdate = new Date()
      pastdate.setDate(pastdate.getDate() - days)
      this.selectedRange.start = pastdate
      this.selectedRange.end = new Date()
      this.update()
    },
    setActive(button) {
      this.buttonIsActive = true
      this.activeBtn = button
    },
    deactivateButton() {
      if (this.buttonIsActive) {
          this.activeBtn = null
          this.buttonIsActive = false
        }
    }
  },
  watch: {
    range(newval) {
      this.selectedRange = newval
    },  
  }
}

</script>


<style>
  
.date-range-bar {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
}

.date-range-bar__buttons {
  display:flex;
  align-items: center;
}

.date-range-bar__buttons > div {
  margin-left: 0.4rem;
}

.date-range-bar__inputs {
  display: flex;
  align-items: center;

}

.date-range-bar__inputs > div:not(:last-child)  {
  margin-right: 0.75rem;
}

.datepicker-field {
  display: flex;
  align-items: center;
}

.datepicker-field > .label {
  margin-bottom: 0;
  margin-right: 0.5rem;

}

</style>