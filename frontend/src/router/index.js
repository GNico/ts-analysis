import VueRouter from 'vue-router'

function lazyLoad(view){
  return() => import(`@/pages/${view}.vue`)
}

let routes = [
	{
		path: '/',
		component: lazyLoad('Home')
	},
	{
		path: '/Visualize',
		component: lazyLoad('Visualize')
	},
	{
		path: '/Anomalies',
		component: lazyLoad('Analysis')
	},
	{
		path: '/Alerts',
		component: lazyLoad('Alerts')
	},
	{
		path: '/Test',
		component: lazyLoad('Test')
	}

];

export default new VueRouter({

	routes,
	linkActiveClass: 'is-active'

});