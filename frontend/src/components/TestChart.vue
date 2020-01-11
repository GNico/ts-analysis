<template>
<div>  



  <highcharts class="chart" v-for="options in optionsList" :key="options.title.text" :options="options" :updateArgs="updateArgs" ref="highcharts"></highcharts>
</div>
</template>

<script>


function sync(vm, event, type) {
  vm.$refs.highcharts.forEach(({ chart }) => {
    if (chart === this.series.chart) return;
    chart.series.forEach((series) => {
      series.data.forEach((point) => {
        if (point.x === this.x) {
          if (type === 'over') {
            point.setState('hover');
            chart.tooltip.refresh(point);
            chart.xAxis[0].drawCrosshair(event, point);
          } else {
            point.setState();
            chart.tooltip.hide();
            chart.xAxis[0].hideCrosshair();
          }
        }
      });
    });
  });
}

function syncExtremes(vm, e) {
  var thisChart = this.chart;
  if (e.trigger !== 'syncExtremes') { // Prevent feedback loop
    vm.$refs.highcharts.forEach(({ chart }) => {
      if (chart !== thisChart) {
        if (chart.xAxis[0].setExtremes) { // It is null while updating
          chart.xAxis[0].setExtremes(e.min, e.max, undefined, false, { trigger: 'syncExtremes' });
        }
      }
    })
  }
}

function genOptions(vm, dataset) {
  let options = {
    chart: {
      marginLeft: 40, // Keep all charts left aligned
      spacingTop: 20,
      spacingBottom: 20,
      zoomType: 'x'
    },
    title: {
      text: dataset.name,
      align: 'left',
      margin: 0,
      x: 30
    },
    credits: {
      enabled: false
    },
    legend: {
      enabled: false
    },
    xAxis: {
      crosshair: true,
      type: 'datetime',
      //plotBands: dataset.results.anomalies,
      events: {
        setExtremes: function(event) {
          syncExtremes.call(this, vm, event);
        },
      },
    },
    yAxis: {
      title: {
        text: null
      }
    },
    tooltip: {
      positioner: function() {
        return {
          // right aligned
          x: this.chart.chartWidth - this.label.width,
          y: 10 // align to title
        };
      },
      borderWidth: 0,
      backgroundColor: 'none',
      pointFormat: '{point.y}',
      headerFormat: '',
      shadow: false,
      style: {
        fontSize: '18px'
      },
      valueDecimals: dataset.valueDecimals
    },
    plotOptions: {
      series: {
        point: {
          events: {
            mouseOver: function(event) {
              sync.call(this, vm, event, 'over');
            },
            mouseOut: function(event) {
              sync.call(this, vm, event, 'out');
            }
          }
        }
      }
    },
    series: [{
      data: dataset.data,
      name: dataset.name,
      type: dataset.type,
      color: dataset.color,
      fillOpacity: 0.3,
      tooltip: {
        valueSuffix: ' ' + dataset.unit
      }
    }]
  };

  if (dataset.results.anomalies) {
    options.xAxis.plotBands = dataset.results.anomalies
  }

  if (dataset.results.baseline) {
    let baseline = {  
      data: dataset.results.baseline, 
      type: 'arearange', 
      color: 'orange',
      lineWidth: 0,
      fillOpacity: 0.3,
      marker: { enabled: false },
      showInLegend: false,
      states: {
          hover: {
              enabled: false
          }
      },
      enableMouseTracking: false
    }
    options.series.push(baseline)
  }

  if (dataset.results.trend) {
    let trend = {
      data: dataset.results.trend,
      type: 'line',
      color: 'white',
      marker: { enabled: false },
      showInLegend: false,
      states: {
          hover: {
              enabled: false
          }
      },
      enableMouseTracking: false
    }
    options.series.push(trend)
  } 

  return options
}


function getColorByvalue(value) {
    let color1 = ''
    let color2 = ''
    if (value<0.5) {
    value = value*2
    color1 = 'e4e814' //center - yellow
    color2 = '00ff00' //left - green
    } else {
    value = (value-0.5)*2
    color1 = 'db1313'  //right - red
    color2 = 'e4e814' //center - yellow
    }
    var hex = function(x) {
      x = x.toString(16);
      return (x.length == 1) ? '0' + x : x;
    };
    var r = Math.ceil(parseInt(color1.substring(0,2), 16) * value + parseInt(color2.substring(0,2), 16) * (1-value));
    var g = Math.ceil(parseInt(color1.substring(2,4), 16) * value + parseInt(color2.substring(2,4), 16) * (1-value));
    var b = Math.ceil(parseInt(color1.substring(4,6), 16) * value + parseInt(color2.substring(4,6), 16) * (1-value));
    return  '#' + (hex(r) + hex(g) + hex(b));
}


/*function anomsToPlotBands(anomalies) {
  var anoms = []
  for (var item of dataset.anomalies) {
    anoms.push({
         from: item.from,
         to: item.to,
         color: item.color,
         events: {
          click: function(e) {
            vm.setActiveAnomaly(this.options.id)
          } 
         }
    })
  }
  return anoms     
} */

export default {
  props: {
    chartsData: {
      default: {},
    }
  },
  data() {
    return { 
      optionsList: [],
      updateArgs: [true, true, {duration: 1000}],
    }
  },
  methods: {
    genChartData() {
      var vm = this;

      this.optionsList = this.chartsData.analysis.map((dataset, i) => {
        if (!("data" in dataset) || dataset.data.length == 0 ) {
          dataset.data = this.chartsData.series 
        }
        dataset.color = 'red';
        dataset.unit = ''
        //add colors to anomalies based on score
        if (dataset.results.anomalies) {
          for (var item of dataset.results.anomalies) {
            item['color'] = getColorByvalue(item.score)
          }
        }
        return genOptions(vm, dataset);
      })

      
    }
  },
  watch: {
    chartsData(newval) {
      this.genChartData();
    }
  }
}


</script>


<style>

.chart {
  min-width: 320px;
  min-height: 300px;
  margin: 0 auto;
}

</style>