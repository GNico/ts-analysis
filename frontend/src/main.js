import Vue from 'vue'
import VueRouter from 'vue-router'
import Highcharts from 'highcharts'
import HighchartsVue from 'highcharts-vue'
import highchartsMore from 'highcharts/highcharts-more'
import Boost from 'highcharts/modules/boost'
import stockInit from 'highcharts/modules/stock'
import router from './router/index'
import store from './store/index'
//import '@mdi/font/css/materialdesignicons.css'
import Buefy from 'buefy'
import App from './App.vue'


Vue.use(HighchartsVue)
Vue.use(VueRouter)
Vue.use(Buefy)
//Vue.use(Buefy, {defaultIconPack: 'fa'})
stockInit(Highcharts)
highchartsMore(Highcharts)
Boost(Highcharts)
//dark theme for highcharts
require('./assets/themes/dark-unica.js');
require('./assets/sass/main.scss');




new Vue({
  el: '#app',
  router: router,
  store: store,
  render: h => h(App)
});
