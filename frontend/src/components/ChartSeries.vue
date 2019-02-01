<template>
    <highcharts class="chart" :options="chartOptions" :updateArgs="updateArgs" ref="chart"></highcharts>
</template>

<script>


export default {
  props: {
    seriesData: {
        default: function () {
          return []
        }
    },
    title: {
        type: String,
        default: ''
    },
    anomalies: {
        type: Array,
        default: function () {
          return []
        }
    },
    isLoading: false,
  },  
  data () {
    return {
      updateArgs: [true, true, {duration: 1000}],
      scoreThreshold: '0',
      bands: [],
      lines: [],
    }
  },
  computed: {
    chartOptions() {
      return {
        chart: {
          zoomType: 'xy',
          panning: true,
          panKey: 'shift'
        },
        credits: false,
        loading: {
          labelStyle: {
              color: 'white',
              fontSize: '1.5rem'
          },
          style: {
              backgroundColor: 'black'
          }
        },
        title: {
          text: this.title
        },
        xAxis: {
          type: 'datetime',
          plotBands: this.bands,
          plotLines: this.lines
        },
        yAxis: {
          title: '',
        },
        rangeSelector: {
          enabled: true
        },
        scrollbar: {
          enabled: true
        },
        legend: {
          enabled: true,
        },
        series: this.seriesData
      }
    },
  },
  methods: {
    selectColor(ratio) {
      let color1 = ''
      let color2 = ''
      if (ratio<0.5) {
        ratio = ratio*2
        color1 = 'FFFF00'
        color2 = '0000FF'
      } else {
        ratio = (ratio-0.5)*2
        color1 = 'FF0000'
        color2 = 'FFFF00'
      }

      var hex = function(x) {
          x = x.toString(16);
          return (x.length == 1) ? '0' + x : x;
      };

      var r = Math.ceil(parseInt(color1.substring(0,2), 16) * ratio + parseInt(color2.substring(0,2), 16) * (1-ratio));
      var g = Math.ceil(parseInt(color1.substring(2,4), 16) * ratio + parseInt(color2.substring(2,4), 16) * (1-ratio));
      var b = Math.ceil(parseInt(color1.substring(4,6), 16) * ratio + parseInt(color2.substring(4,6), 16) * (1-ratio));

      return hex(r) + hex(g) + hex(b);
    },
    parseAnomalies () {
        let anomaly = this.anomalies
        let interval = 3600000
        let bands = []
        let lines = []
        let time = anomaly[0][0]
        let score = anomaly[0][1]
        let newtime = 0
        let newscore = 0
        let start = 0
        let end = 0
        let maxIntervalScore = 0
        let scoreColor = ''

        for (var i = 1; i < anomaly.length; i++) {
            newtime = anomaly[i][0]
            newscore = anomaly[i][1]
            let dif = newtime-time   
            if (start == 0) {
                if (dif > interval) {  // es punto anomalo
                    scoreColor = "#" + this.selectColor(score)
                    if (score > this.scoreThreshold) {
                      lines.push({color: scoreColor, value: time, width: 2})
                    }
                } else {  //comienza un intervalo anomalo
                    start = time
                    maxIntervalScore = score
                }
            } else if (dif > interval) { //termina el intervalo
                end = time
                scoreColor = "#" + this.selectColor(maxIntervalScore)
                if (maxIntervalScore > this.scoreThreshold) {
                  bands.push({color: scoreColor, from: start, to: end})
                }
                start = 0
                end = 0
                maxIntervalScore = 0
            } else {  //continua el intervalo 
                if (maxIntervalScore < score) {
                  maxIntervalScore = score
                }
            }
            time = newtime
            score = newscore
        }

        this.bands = bands
        this.lines = lines
    },
  },
  watch: {
    anomalies() {
      this.parseAnomalies()
    },
    isLoading() {
        if (this.isLoading) {
          this.$refs.chart.chart.showLoading()
        } else {
          this.$refs.chart.chart.hideLoading()
        }
    }
    
  }
}
</script>

