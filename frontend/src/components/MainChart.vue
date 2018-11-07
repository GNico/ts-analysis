<template>
  <div class="chartElem">
    <div class="row">
      <highcharts class="chart" :options="chartOptions" :updateArgs="updateArgs"></highcharts>
      <div>
        <button v-on:click="loadData">Cargar data</button>
        <tag-selector :opciones="seriesTags" v-on:tagchanged="changeSeries"> </tag-selector>
        <button v-on:click="loadAnomalies">Cargar anomalias </button>
      </div>
    </div>
    <div class="row">

      <div v-if="anomalies">
        <gradient-slider v-on:valuechanged="filterScore"> </gradient-slider>
        <div class="color-box" v-bind:style="bgc"></div>
      </div>

      <div id="chartType">
        <h3>Select chart type:</h3>
        <select v-model="chartType">
          <option>Line</option>
          <option>AreaSpline</option>
          <option>Spline</option>
          <option>Scatter</option>
          <option>Column</option>
          <option>Area</option>
        </select>
      </div>

      <div id="seriesColor">
        <h3>Select color of the series:</h3>
        <div class="row">
          <input id="colorPicker" v-if="colorInputIsSupported" type="color" value="#6fcd98" v-model="seriesColor">
          <select v-else v-model="seriesColor">
            <option>Red</option>
            <option>Green</option>
            <option>Blue</option>
            <option>Pink</option>
            <option>Orange</option>
            <option>Brown</option>
            <option>Black</option>
            <option>Purple</option>
          </select>
        </div>
        <p>Current color: {{seriesColor}}</p>
      </div>

    </div>
  </div>
</template>

<script>

import TagSelector from './TagSelector.vue'
import GradientSlider from './GradientSlider.vue'


function selectColor(ratio) {
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

}


export default {
  components: { TagSelector, GradientSlider },
  data () {
    return {

      bgc: {
        backgroundColor: ''
      },

      scoreThreshold: '0',

      anomalies: null,

      seriesTags: [],
      currentTag: '',
      title: '',
      points: [],
      chartType: 'line',
      seriesColor: '#6fcd98',
      colorInputIsSupported: null,
      updateArgs: [true, true, {duration: 1000}],
      chartOptions: {
        chart: {
          type: 'line',
          zoomType: 'xy',
          panning: true,
        },
        title: {
          text: 'Eventos totales'
        },
        xAxis: {
            type: 'datetime'
        },
        yAxis: {
            title: ''
        },
        rangeSelector: {
            enabled: true
        },
        scrollbar: {
            enabled: true
        },
        series: [{
          data: [],
          color: '#6fcd98'
        }]
      }
    }
  },
  created () {
    let i = document.createElement('input')
    i.setAttribute('type', 'color');
    (i.type === 'color') ? this.colorInputIsSupported = true : this.colorInputIsSupported = false
  },
  methods: {
    loadData () {
        this.currentTag = ''
        var vm = this;
        let requestUrl = hosturl + 'series/'
        axios.get(requestUrl)
            .then(function (response) {
                vm.chartOptions.series[0].data = response.data
            })
            .catch(function (error) {
                console.log(error);
            });

        //get tags list
        requestUrl = hosturl + 'tags/'
        axios.get(requestUrl)
            .then(function (response) {
                vm.seriesTags = response.data
            })
            .catch(function (error) {
                console.log(error);
            });

    },
    loadAnomalies () {
        var vm = this;
        let requestUrl = hosturl + 'anomaly/'
        if (this.currentTag) {
            requestUrl += ('?tag=' + this.currentTag)
        }
        axios.get(requestUrl)
            .then(function (response) {
                vm.anomalies = response.data
            })
            .catch(function (error) {
                console.log(error);
            });
    },
    parseAnomalies (anomaly) {
        var interval = 1800000
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
                    scoreColor = "#" + selectColor(score)
                    if (score > this.scoreThreshold) {
                      lines.push({color: scoreColor, value: time, width: 2})
                    }
                } else {  //comienza un intervalo anomalo
                    start = time
                    maxIntervalScore = score
                }
            } else if (dif > interval) { //termina el intervalo
                end = time
                scoreColor = "#" + selectColor(maxIntervalScore)
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

        this.chartOptions.xAxis.plotBands = bands
        this.chartOptions.xAxis.plotLines = lines
        this.title = (this.currentTag ? this.currentTag : 'Eventos totales' ) + ' + anomalies above ' + this.scoreThreshold + ' score' 

    },
    changeSeries (payload) {
        let requestUrl = hosturl + 'series/'
        this.currentTag = payload.selected
        if (this.currentTag) {
            requestUrl += ('?tag=' + this.currentTag)
        }

        this.chartOptions.xAxis.plotBands = []
        this.chartOptions.xAxis.plotLines = []
        this.title = (this.currentTag ? this.currentTag : 'Serie total' )

        var vm = this;
        axios.get(requestUrl)
            .then(function (response) {
                vm.chartOptions.series[0].data = response.data
                vm.title = selectedTag
            })
            .catch(function (error) {
                console.log(error);
            });
    },
    filterScore (payload) {
        let w = payload.value / 100
        this.bgc.backgroundColor = "#" + selectColor(w) 

        this.scoreThreshold = w
    }
  },
  watch: {
    title (newValue) {
      this.chartOptions.title.text = newValue
    },
    chartType (newValue) {
      this.chartOptions.chart.type = newValue.toLowerCase()
    },
    seriesColor (newValue) {
      this.chartOptions.series[0].color = newValue.toLowerCase()
    },
    scoreThreshold (newValue) {
      this.parseAnomalies(this.anomalies)
    },
    anomalies (newValue) {
      this.parseAnomalies(newValue)
    }
  }
}
</script>


<style>

.color-box {
    width: 25px;
    height: 25px;
    display: inline-block;
}

</style>