var placeholder = [
        [1299456000000,50.77],
        [1299542400000,50.82],
        [1299628800000,50.35],
        [1299715200000,49.52],
        [1299801600000,50.28],
        [1300060800000,50.51],
        [1300147200000,49.35],
        [1300233600000,47.14],
        [1300320000000,47.81],
        [1300406400000,47.24],
        [1300665600000,48.47],
        [1300752000000,48.74],
        [1300838400000,48.46],
        [1300924800000,49.28],
        [1301011200000,50.22],
        [1301270400000,50.06],
        [1301356800000,50.14],
        [1301443200000,49.80],
        [1301529600000,49.79],
        [1301616000000,49.22],
        [1301875200000,48.74],
        [1301961600000,48.41],
        [1302048000000,48.29],
        [1302134400000,48.30],
        [1302220800000,47.87],
        [1302480000000,47.26],
        [1302566400000,47.49],
        [1302652800000,48.02],
        [1302739200000,47.49],
        [1302825600000,46.78],
        [1303084800000,47.41],
        [1303171200000,48.27],
        [1303257600000,48.92],
        [1303344000000,50.10],
        [1303689600000,50.43],
        [1303776000000,50.06],
        [1303862400000,50.02],
        [1303948800000,49.54],
        [1304035200000,50.02],
        [1304294400000,49.47],
        [1304380800000,49.74],
        [1304467200000,49.94],
        [1304553600000,49.54],
        [1304640000000,49.52],
        [1304899200000,49.66],
        [1304985600000,49.92],
        [1305072000000,49.60],
        [1305158400000,49.51],
        [1305244800000,48.64],
        [1305504000000,47.61]
]

var anomaly = [
        [1299628800000,50.35],
        [1299801600000,50.28],
        [1300233600000,47.14],
        [1300838400000,48.46],
        [1300924800000,49.28],
        [1302652800000,48.02],
        [1302739200000,47.49],
        [1302825600000,46.78],
        [1303084800000,47.41],
]
/**
 * Display a temporary label on the chart
 */
function toast(chart, text) {
    chart.toast = chart.renderer.label(text, 100, 120)
        .attr({
            fill: Highcharts.getOptions().colors[0],
            padding: 10,
            r: 5,
            zIndex: 8
        })
        .css({
            color: '#FFFFFF'
        })
        .add();

    /*setTimeout(function () {
        chart.toast.fadeOut();
    }, 2000);
    setTimeout(function () {
        chart.toast = chart.toast.destroy();
    }, 2500); */
}

/**
 * Custom selection handler that selects points and cancels the default zoom behaviour
 */
function selectPointsByDrag(e) {
    // Select points
    
    try {
        if (shiftdown) {

            Highcharts.each(this.series, function (series) {
                Highcharts.each(series.points, function (point) {
                    if (point.x >= e.xAxis[0].min && point.x <= e.xAxis[0].max &&
                            point.y >= e.yAxis[0].min && point.y <= e.yAxis[0].max) {
                        point.select(null, true);
                    }
                });
            }); 
            // Fire a custom event
            Highcharts.fireEvent(this, 'selectedpoints', { points: this.getSelectedPoints() });

            return false;  // Don't zoom
        }
    } catch(err) {
        //do nothing
    }
}

/**
 * The handler for a custom event, fired from selection event
 */
function selectedPoints(e) {
    // Show a label
    toast(this, '<b>' + e.points.length + ' points selected.</b>' +
        '<br>Deseleccionar no implementado');
}

/**
 * On click, unselect all points
 */
function unselectByClick() {
    var points = this.getSelectedPoints();
    if (points.length > 0) {
        Highcharts.each(points, function (point) {
            point.select(false);
        });
    }
}

var shiftdown = false;


//register component 
Vue.component('seriesselector', {
    template: '<select v-model="selected" v-on:change="tagselected"> <option v-for="option in opciones" v-bind:value="option"> {{ option }} </option> </select>',
    props: ['opciones'],
    data: function() {
        return {
            selected: ''
        }
    },
    methods: {
        tagselected: function() {
            this.$emit('tagchanged', {selected: this.selected})
        }
    }
})

var vm = new Vue({
    el: "#app",
    data: {
        chart: undefined,
        chart2: undefined,
        chartdata2: [],
        chartdata: [],
        fulldata: [],
        seriestags: [],
        tagsdata: [],
        config: {
            chart: {
                events: {
                    selection: selectPointsByDrag,
                    selectedpoints: selectedPoints,
                },
                zoomType: 'xy'
            },
            title: {
                text: 'Tags'
            },
            subtitle: {
                text: document.ontouchstart === undefined ?
                        'Click and drag in the plot area to zoom in' : 'Pinch the chart to zoom in'
            },
            xAxis: {
                type: 'datetime'
            },
            yAxis: {
                title: {
                    text: ''
                }
            },
            legend: {
                enabled: false
            },
            navigator: {
                enabled: true      
            },
            scrollbar: {
                enabled: true
            },
            rangeSelector: {
                enabled: true
            },
            series: [{
                type: 'line',
                allowPointSelect: true,
                marker: {
                    radius:1,
                    states: {
                        select: {
                            radius:5,
                            fillColor: 'red',
                        }
                    }
                },
                states: {
                    hover: {
                        lineWidth: 1
                    }
                },
            }]
        },
        //shiftdown: false
    },
    created: function() {
        document.addEventListener('keydown', this.shiftKeydownListener);
        document.addEventListener('keyup', this.shiftKeyupListener);

    },
    mounted() {
        this.getData();
        this.render();
    },
    destroyed: function() {
        document.removeEventListener('keydown', this.shiftKeydownListener);
        document.removeEventListener('keyup', this.shiftKeyupListener);
    },
    watch: {
        chartdata() {
            this.chart.series[0].setData(this.chartdata, true)
        },
        chartdata2() {
            this.chart2.series[0].setData(this.chartdata2, true)
            //this.chart2.addSeries({                        
            //    type: 'scatter',
            //    color: 'red',
            //    data: anomaly
            //});
            //this.chart2.series[1].update(newchartoptions);
            //console.log(this.chart2.series[1]);
        },
        config() {
            this.render();
        },
    },
    methods: {
        render() {
            this.chart = Highcharts.chart('container', this.config)
            this.chart2 = Highcharts.chart('container2', this.config)
        },
        getData() {
            var vm = this;
            axios.get('/prueba/tags/')
            .then(function (response) {
                //vm.fulldata = response.data
                vm.seriestags = response.data;
                //vm.chartdata = response.data[vm.seriestags[0]];
            })
            .catch(function (error) {
                console.log(error);
            });

            axios.get('/prueba/data/')
            .then(function (response) {
                vm.chartdata2 = response.data;
            })
            .catch(function (error) {
                console.log(error);
            });
           
            //vm.chartdata2 = placeholder;
            //this.chart2.series[1].setData(anomaly, true)
        },
        changeSeries: function(payload) {
            selectedTag = payload.selected;
            var vm = this;
            axios.get('/prueba/series/', {
    			params: {
      				tag: selectedTag
    			}
    		})
            .then(function (response) {
                vm.chartdata = response.data;
                vm.chart.setTitle({text: selectedTag});
            })
            .catch(function (error) {
                console.log(error);
            });
        },
        shiftKeydownListener: function(evt) {
            if (evt.keyCode === 16) {
            shiftdown = true;
          }
        },
        shiftKeyupListener: function(evt) {
            if (evt.keyCode === 16) {
            shiftdown = false;
          }
        }
    }
});
