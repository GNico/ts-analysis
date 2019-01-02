<template>

<div class="level">

  <div class="level-left">

    <div class="buttons">
      <button class="button is-primary" :class="{ 'is-info': activeBtn === 'btn1' }" @click="setAll(); setActive('btn1')" >
        Todo
      </button>       
      <button class="button is-primary" :class="{ 'is-info': activeBtn === 'btn2' }" @click="setLast(365); setActive('btn2')" >
        Ultimo año
      </button>
      <button class="button is-primary" :class="{ 'is-info': activeBtn === 'btn3' }" @click="setLast(30); setActive('btn3')" >
        Ultimos 30 dias
      </button>
      <button class="button is-primary" :class="{ 'is-info': activeBtn === 'btn4' }" @click="setLast(7); setActive('btn4')" >
        Ultimos 7 dias
      </button> 
      <button class="button is-primary" :class="{ 'is-info': activeBtn === 'btn5' }" @click="setLast(1); setActive('btn5')" >
        Ultimo dia
      </button>
    </div>       
  </div>

  <div class="level-right">

    <div class="level-item">
      <label class="label">Desde</label>
    </div>
    <div class="level-item">
      <b-datepicker v-model="selectedRange.start"
          :first-day-of-week="1"
          placeholder="Click para seleccionar...">

          <button class="button is-primary"
              @click="selectedRange.start = new Date()">
              <b-icon icon="calendar-today"></b-icon>
              <span>Hoy</span>
          </button>

          <button class="button is-danger"
              @click="selectedRange.start = null">
              <b-icon icon="close"></b-icon>
              <span>Borrar</span>
          </button>
      </b-datepicker>
    </div>

    <div class="level-item">
      <label class="label">Hasta</label>
    </div>
    <div class="level-item">
      <b-datepicker v-model="selectedRange.end"
          :first-day-of-week="1"
          placeholder="Click para seleccionar...">

          <button class="button is-primary"
              @click="selectedRange.end = new Date()">
              <b-icon icon="calendar-today"></b-icon>
              <span>Hoy</span>
          </button>

          <button class="button is-danger"
              @click="selectedRange.end = null">
              <b-icon icon="close"></b-icon>
              <span>Borrar</span>
          </button>
      </b-datepicker>
    </div>

    <div class="level-item">
      <button class="button is-primary" @click="update">
        Actualizar
      </button>                   
    </div>

  </div>
</div>
</template>


<script>

export default {
  name: "DateRangeSelect",
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
  /*watch: {
    selectedRange: {
      handler(newVal) {
        this.$emit('input', { start: this.selectedRange.start, end: this.selectedRange.end })
      },
      deep: true
    }
  }*/
}

</script>