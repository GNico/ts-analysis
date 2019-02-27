import VueRouter from 'vue-router'


let routes = [
	{
		path: '/',
		component: require('@/pages/Home.vue').default
	},
	{
		path: '/Visualize',
		component: require('@/pages/Visualize.vue').default
	},
	{
		path: '/Anomalies',
		component: require('@/pages/Analysis.vue').default
	},
	{
		path: '/Alerts',
		component: require('@/pages/Alerts.vue').default

	}

];

export default new VueRouter({

	routes,
	linkActiveClass: 'is-active'

});