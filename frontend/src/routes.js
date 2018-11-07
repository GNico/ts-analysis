import VueRouter from 'vue-router'


let routes = [
	{
		path: '/',
		component: require('./pages/Home.vue').default
	},
	{
		path: '/Alerts',
		component: require('./pages/Alerts.vue').default

	}

];

export default new VueRouter({

	routes,
	linkActiveClass: 'is-active'

});