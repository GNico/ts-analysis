import VueRouter from 'vue-router'
import Index from '@/pages/monitoring/Index.vue'

function lazyLoad(view){
  return () => import(`@/pages/${view}.vue`)
}

let routes = [
  {
    path: '/',
    component: lazyLoad('DataManagement')
  },
  {
    path: '/Visualization',
    component: lazyLoad('Visualization')
  },
  {
    path: '/Analysis',
    component: lazyLoad('Analysis')
  },
  {
    path: '/Monitoring',
    component: Index,
    children: [
      {
        component: lazyLoad("monitoring/Incidents"),
        path: 'Incidents'
      },
      {
        component: lazyLoad("monitoring/Monitors"),
        path: 'Monitors'
      },
    ] 
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
