import Vue from 'vue'
import HighchartsVue from 'highcharts-vue'
import Highcharts from 'highcharts'
import stockInit from 'highcharts/modules/stock'
import axios from 'axios'
import VueRouter from 'vue-router'
import App from './App.vue'
import router from './routes'

stockInit(Highcharts)

Vue.use(HighchartsVue)
Vue.use(VueRouter)

// Require the main Sass manifest file
require('./assets/sass/main.scss');

window.axios = axios
window.hosturl = 'http://localhost:8000/prueba/'

new Vue({
  el: '#app',
  router: router,
  render: h => h(App)
});
