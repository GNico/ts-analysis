import Vue from 'vue'
import VueRouter from 'vue-router'
import Highcharts from 'highcharts'
import HighchartsVue from 'highcharts-vue'
import Boost from 'highcharts/modules/boost'
import App from './App.vue'
import router from './router/index'
import store from './store/index'
import Buefy from 'buefy'

Vue.use(HighchartsVue)
Boost(Highcharts)
Vue.use(VueRouter)
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
