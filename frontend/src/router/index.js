import VueRouter from 'vue-router'

function lazyLoad(view){
  return() => import(`@/pages/${view}.vue`)
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
    component: lazyLoad('Monitoring')
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