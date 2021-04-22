import VueRouter from 'vue-router'
import Index from '@/pages/monitoring/Index.vue'
import MonitorDetails from '@/components/monitoring/MonitorDetails.vue'
import MonitorTable from '@/components/monitoring/MonitorTable.vue'

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
            component: MonitorTable
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
  {
    path: '/Test',
    component: lazyLoad('Test')
  } 
];

export default new VueRouter({
  routes,
  linkActiveClass: 'is-active'
});
