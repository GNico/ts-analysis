import Vue from 'vue'
import VueRouter from 'vue-router'
import Highcharts from 'highcharts'
import HighchartsVue from 'highcharts-vue'
import highchartsMore from 'highcharts/highcharts-more'
import Boost from 'highcharts/modules/boost'

import DragPanes from 'highcharts/modules/drag-panes'
import App from './App.vue'
import router from './router/index'
import store from './store/index'
//import '@mdi/font/css/materialdesignicons.css'
import Buefy from 'buefy'

import stockInit from 'highcharts/modules/stock'
stockInit(Highcharts)

Vue.use(HighchartsVue)
highchartsMore(Highcharts)
Boost(Highcharts)
DragPanes(Highcharts)
Vue.use(VueRouter)
//Vue.use(Buefy, {defaultIconPack: 'fa'})
Vue.use(Buefy)
//dark theme for highcharts
require('./assets/themes/dark-unica.js');

require('./assets/sass/main.scss');

new Vue({
  el: '#app',
  router: router,
  store: store,
  render: h => h(App)
});
