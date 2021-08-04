<template>
<div>
  <div class="my-4">
    <div class="tile is-ancestor has-text-centered">
      <div class="tile is-parent">
        <article class="tile is-child box has-background-grey-dark notification-tile">
          <p class="title is-4">{{total}}</p>
          <p class="subtitle">Total events</p>
        </article>        
      </div>
      <div class="tile is-parent">
        <article class="tile is-child box has-background-grey-dark notification-tile">
          <p class="title is-4">{{weeklyAverage}}</p>
          <p class="subtitle">Weekly events (avg)</p>
        </article>
      </div>
      <div class="tile is-parent">
        <article class="tile is-child box has-background-grey-dark notification-tile">
          <p class="title is-4">{{rangeData.start}}</p>
          <p class="subtitle">Oldest event</p>
        </article>
      </div>
      <div class="tile is-parent">
        <article class="tile is-child box has-background-grey-dark notification-tile">
          <p class="title is-4">{{rangeData.end}}</p>
          <p class="subtitle">Latest event</p>
        </article>
      </div>      
    </div>
  </div>

  <div class="columns">
    <div class="column is-8">
      <highcharts  :options="chartOptions" :updateArgs="updateArgs" />
    </div>

    <div class="column is-4">
      <div class="card events-card">
        <header class="card-header">
          <p class="card-header-title">
              Most recent events
          </p>
          <a href="#" class="card-header-icon" aria-label="more options">
          <span class="icon">
            <i class="fa fa-angle-down" aria-hidden="true"></i>
          </span>
          </a>
        </header>
        <div class="card-table">
          <div class="content">
            <table class="table is-fullwidth is-striped">
              <tbody>
                <tr v-for="event in lastEvents">
                  <td>
                    <div><i class="mdi mdi-calendar"></i> {{ formatDate(event[0]) }}</div>
                    <div class="tags is-flex is-flex-wrap-nowrap">
                      <i class="mdi mdi-tag-multiple mr-1"></i> 
                      <span v-if="!event[1].length"> No tags </span>
                      <span v-else v-for="tag in event[1]" class="tag is-primary">{{tag}}</span>
                    </div>
                  </td>
                </tr>              
              </tbody>
            </table>
          </div>
        </div>        
      </div>
    </div>
  </div>
</div>
</template>


<script>
import { formatDate } from '../utils/dateFormatter'

export default {
  props: {
    name: {
      type: String,
      required: true,
    },
    clientDetails: {
      type: Object,
      required: true,
    }
  }, 
  data() {
    return {
      updateArgs: [true, true, false],  
    }
  },
  computed: {
    details() {
      return this.clientDetails.hasOwnProperty(this.name) ? this.clientDetails[this.name] : { data: [], range: {}, tagsCount: 0, lastEvents: []}
    },
    seriesData() {
      return this.details.data.map(x => [x[0] + 604800000, x[1]])  //adding a week offset
    }, 
    rangeData() {
      return { 
        start: this.details.range.hasOwnProperty("start") ? this.formatDate(this.details.range.start) : '-',
        end: this.details.range.hasOwnProperty("end") ? this.formatDate(this.details.range.end) : '-'
      }
    },
    total() {
      return this.details.total
    },
    lastEvents() {
      return this.details.lastEvents
    },
    weeklyAverage() {
      if (this.seriesData.length == 0) return 0
      let average = this.seriesData.map(x => x[1]).reduce((a,b) => a + b, 0)
      return Math.round(average / this.seriesData.length)
    },
    chartOptions() {
      return {
        chart: {
          backgroundColor: '#073642',
          borderColor: '#003f50',
          borderWidth: 2,
          borderRadius: 5,
          height: 400,
        },
        title: '',
        credits: false,  
        xAxis: {
          type: 'datetime'
        },
        yAxis: {
          title: ''
        },
        legend: {
          enabled: false,
        },
        plotOptions: {
          column: {
            groupPadding: 0,
            pointPadding: 0,
            borderWidth: 1,
            borderColor: 'lightblue'
          }
        },
        series: [{
          type: 'column',
          data: this.seriesData
        }]
      }
    }
  },
  methods: {
    formatDate(input) {
      return formatDate(input)
    }
  },
  watch: { 
    isOpen() {
      console.log(this.isOpen)
    }
  },
}

</script>


<style>
.events-card .card-table {
  max-height: 350px;
  max-width: 400px;
  width: inherit;
  overflow-y: auto;
  overflow-x: auto;
}

.notification-tile {
  border: 2px solid #003f50;
}
</style>