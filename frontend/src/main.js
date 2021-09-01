import Vue from 'vue'
import VueRouter from 'vue-router'
import Highcharts from 'highcharts'
import HighchartsVue from 'highcharts-vue'
import highchartsMore from 'highcharts/highcharts-more'
//import Boost from 'highcharts/modules/boost'
import stockInit from 'highcharts/modules/stock'
import heatmap from 'highcharts/modules/heatmap'
import router from './router/index'
import store from './store/index'
import Buefy from 'buefy'
import App from './App.vue'


Vue.use(HighchartsVue)
Vue.use(VueRouter)
Vue.use(Buefy)
stockInit(Highcharts)
heatmap(Highcharts)
highchartsMore(Highcharts)
//Boost(Highcharts)
require('./assets/themes/dark-unica.js'); //dark theme for highcharts
require('./assets/sass/main.scss');


new Vue({
  el: '#app',
  router: router,
  store: store,
  render: h => h(App)
});
