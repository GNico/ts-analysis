<template>

<div>

  <b-modal 
    :active.sync="isOpenAddSeries" 
    has-modal-card 
    :can-cancel="['escape', 'outside']" 
    animation='' 
    scroll='keep'>
    <div class="modal-content">
      <VisualizeCardSeries @close="isOpenAddSeries=false"/>
    </div>
  </b-modal>

  <b-modal 
    :active.sync="isOpenSettings" 
    has-modal-card 
    :can-cancel="['escape', 'outside']" 
    animation='' 
    scroll='keep'>
    <div class="modal-content">
      <VisualizeCardSettings/>
    </div>
  </b-modal>

  <div class="level">
    <div class="level-left has-text-weight-semibold">
      <a class="level-item button is-info is-small" 
        @click="isOpenAddSeries = true"
        :class="isOpenAddSeries ? '' : 'is-outlined'">
        <b-icon icon="chart-line" size=""></b-icon><span>Add series</span>
      </a>          

      <a class="level-item button is-info is-outlined is-small">
        <b-icon icon="finance"></b-icon>
        <span>Indicators</span>
      </a>

      <a class="level-item button is-info is-small"
        @click="isOpenSettings = true"
        :class="isOpenSettings ? '' : 'is-outlined'">
        <b-icon icon="cog"></b-icon><span>Settings</span>
      </a>

      <a class="level-item button is-info is-outlined is-small">
        <b-icon icon="fullscreen"></b-icon>
      </a>
    </div>

    <div class="level-right toolbar-right">
      <div class="level-item datepicker-field">
        <label class="label">From</label>
        <b-datepicker             
            :first-day-of-week="1"
            placeholder="Click to select..."
            size="is-small"
            @input="">

            <button class="button is-primary is-small"
                @click="selectedRange.start = new Date()">
                <b-icon  icon="calendar-today" size="is-small"></b-icon>
                <span>Today</span>
            </button>

            <button class="button is-danger is-small"
                @click="selectedRange.start = null">
                <b-icon icon="close-thick" size="is-small"></b-icon>
                <span>Clear</span>
            </button>
        </b-datepicker>
      </div>

      <div class="level-item datepicker-field">
        <label class="label">To</label>
        <b-datepicker          
            :first-day-of-week="1"
            placeholder="Click to select..."
            size="is-small"
            @input="">

            <button class="button is-primary is-small"
                @click="selectedRange.end = new Date()">
                <b-icon icon="calendar-today" size="is-small"></b-icon>
                <span>Today</span>
            </button>

            <button class="button is-danger is-small"
                @click="selectedRange.end = null">
                <b-icon icon="close-thick" size="is-small"></b-icon>
                <span>Clear</span>
            </button>
        </b-datepicker>
      </div>

      <div>
        <a class="button is-primary is-small" @click="update">
          <b-icon icon="refresh"/>
          <span>Update</span>
        </a> 
      </div>  

      <div>
        <a class="button is-primary is-small">
          <b-icon icon="dots-vertical"/>
        </a> 
      </div>

    </div>
  </div>

</div>

</template>


<script>
import VisualizeCardSeries from './VisualizeCardSeries.vue';
import VisualizeCardSettings from './VisualizeCardSettings.vue';


export default {
  components: { VisualizeCardSeries, VisualizeCardSettings },
  data () {
    return {
      isOpenAddSeries: false,
      isOpenSettings: false,
    }
  },
  methods: {
    update() {

    }
  }
}
</script>



<style scoped>

.toolbar-right {
  display: flex;
  align-items: center;

}

.toolbar-right > div:not(:last-child)  {
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