<template>
<div class="date-range-bar" >

    <div class="date-range-bar__buttons">
      <button class="button is-primary" :class="{ 'is-info': activeBtn === 'btn1' }" @click="setActive('btn1'); setAll()" >
        Todo
      </button>       
      <button class="button is-primary" :class="{ 'is-info': activeBtn === 'btn2' }" @click="setActive('btn2'); setLast(365)" >
        Ultimo año
      </button>
      <button class="button is-primary" :class="{ 'is-info': activeBtn === 'btn3' }" @click="setActive('btn3'); setLast(30)" >
        Ultimos 30 dias
      </button>
      <button class="button is-primary" :class="{ 'is-info': activeBtn === 'btn4' }" @click="setActive('btn4'); setLast(7)" >
        Ultimos 7 dias
      </button> 
      <button class="button is-primary" :class="{ 'is-info': activeBtn === 'btn5' }" @click="setActive('btn5'); setLast(1)" >
        Ultimo dia
      </button>
    </div>       

    <div class="date-range-bar__inputs">
      <div class="datepicker-field">
        <label class="label">Desde</label>
        <b-datepicker 
            v-model="selectedRange.start"
            icon-pack="fas"
            :first-day-of-week="1"
            placeholder="Click para seleccionar...">

            <button class="button is-primary"
                @click="selectedRange.start = new Date()">
                <b-icon pack="fas" icon="calendar-day"></b-icon>
                <span>Hoy</span>
            </button>

            <button class="button is-danger"
                @click="selectedRange.start = null">
                <b-icon pack="fas" icon="times"></b-icon>
                <span>Borrar</span>
            </button>
        </b-datepicker>
      </div>

      <div class="datepicker-field">
        <label class="label">Hasta</label>
        <b-datepicker 
            v-model="selectedRange.end"
            icon-pack="fas"
            :first-day-of-week="1"
            placeholder="Click para seleccionar...">

            <button class="button is-primary"
                @click="selectedRange.end = new Date()">
                <b-icon pack="fas" icon="calendar-day"></b-icon>
                <span>Hoy</span>
            </button>

            <button class="button is-danger"
                @click="selectedRange.end = null">
                <b-icon pack="fas" icon="times"></b-icon>
                <span>Borrar</span>
            </button>
        </b-datepicker>

      </div>

      <div>
        <button class="button is-primary" @click="update">
          Actualizar
        </button> 
      </div>  
    </div>                
</div>

</template>


<script>

export default {
  props: {
      value: {
        type: Object,
      }
  },
  data () {
    return {
      selectedRange: {
        start: this.value.start,
        end: this.value.end,
      },
      activeBtn: ''
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
      this.activeBtn = button
    }
  },
}

</script>


<style>
  
.date-range-bar {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
}

.date-range-bar__buttons {
  padding-right: 1rem;
}

.date-range-bar__inputs {
  display: flex;
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