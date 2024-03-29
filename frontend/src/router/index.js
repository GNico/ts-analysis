import VueRouter from 'vue-router'
import MonitorDetails from '@/components/monitoring/MonitorDetails.vue'

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
    component: lazyLoad('monitoring/Index'),
    children: [
      {
        path: '', 
        beforeEnter: (to, from, next) => next('/Monitoring/Incidents')
      },
      {
        path: 'Incidents',
        component: lazyLoad("monitoring/Incidents")
      },
      {                
        path: 'Monitors',
        component: lazyLoad("monitoring/Monitors"),
        children: [
          {
            path: '',
            component: () => import(`@/components/monitoring/MonitorTable.vue`)
          },
          {
            name: 'MonitorDetails',
            path: ':id',
            component: MonitorDetails
          }
        ]
      },
    ] 
  },
];

export default new VueRouter({
  routes,
  linkActiveClass: 'is-active'
});
