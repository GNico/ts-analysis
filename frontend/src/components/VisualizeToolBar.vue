<template>
<div>

  <component
    v-for="item in options"
    :key="item.name"
    :is="item.component"
    :isActive="item.open"
    @close="item.open=false"/>

  <div class="level">
    <div class="level-left has-text-weight-semibold">
      <a v-for="item in options" 
        :key="item.name"
        class="level-item button is-info is-small" 
        @click="item.open = true"
        :class="item.open ? '' : 'is-outlined'">
        <b-icon :icon="item.icon" size=""></b-icon>
        <span>{{item.name}}</span>
      </a>          

      <a class="level-item button is-info is-outlined is-small" @click="$emit('refresh')">
        <b-icon icon="refresh"></b-icon><span>Refresh</span>
      </a>
    </div>

    <div class="level-right toolbar-right">
      <div class="level-item datepicker-field">
        <label class="label">From</label>
        <b-datepicker             
            :first-day-of-week="1"
            placeholder="Click to select..."
            size="is-small"
            v-model="selectedRange.start">

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
            v-model="selectedRange.end">

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
        <b-dropdown aria-role="list" position="is-bottom-left">
            <a class="button is-primary is-small" slot="trigger">
              <b-icon icon="dots-vertical"/>
            </a>
            <b-dropdown-item aria-role="listitem">Last day</b-dropdown-item>
            <b-dropdown-item aria-role="listitem">Last week</b-dropdown-item>
            <b-dropdown-item aria-role="listitem">Last month</b-dropdown-item>
            <b-dropdown-item aria-role="listitem">Last year</b-dropdown-item>
        </b-dropdown>
      </div>
    </div>
  </div>
</div>
</template>


<script>

import VisualizeCardSeries from './VisualizeCardSeries.vue';
import VisualizeCardIndicators from './VisualizeCardIndicators.vue';
import VisualizeCardSettings from './VisualizeCardSettings.vue';
import ModalCard from './ModalCard.vue';

export default {
  components: { VisualizeCardSeries, VisualizeCardIndicators, VisualizeCardSettings, ModalCard},
  data () {
    return {
      selectedRange: {
        start: null,
        end: null
      },
      options: [
        {
          name: 'Add series',
          icon: 'chart-line',        
          component: 'VisualizeCardSeries',
          open: false,
        },
    /*    {
          name: 'Indicators',
          icon: 'finance',        
          component: 'VisualizeCardIndicators',
          open: false,
        }, */
        {
          name: 'Settings',
          icon: 'cog',        
          component: 'VisualizeCardSettings',
          open: false,
        }
      ],
    }
  },
  computed: {
    range() {
       return this.$store.state.visualize.range
    }
  },
  methods: {
    update() {
      this.$store.dispatch('visualize/updateRange', this.selectedRange)
    }
  },
  watch: {
    range: {
      immediate: true,
      handler: function (newVal) {
        this.selectedRange.start = newVal.start
        this.selectedRange.end = newVal.end
      }  
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

.options-card {
  overflow-y: auto;
}

</style>