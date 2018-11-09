import Vue from 'vue'
import VueRouter from 'vue-router'
import HighchartsVue from 'highcharts-vue'
import axios from 'axios'
import App from './App.vue'
import router from './router/index'
import store from './store/index'
import VueCtkDateTimePicker from 'vue-ctk-date-time-picker';
import 'vue-ctk-date-time-picker/dist/vue-ctk-date-time-picker.min.css';

Vue.use(HighchartsVue)

Vue.use(VueRouter)

Vue.component('vue-ctk-date-time-picker', VueCtkDateTimePicker);

//dark theme for highcharts
require('./assets/themes/dark-unica.js');

// Require the main Sass manifest file
require('./assets/sass/main.scss');

window.axios = axios
window.hosturl = 'http://localhost:8000/prueba/'

new Vue({
  el: '#app',
  router: router,
  store: store,
  render: h => h(App)
});
