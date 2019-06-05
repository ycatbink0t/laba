import Vue from 'vue'
import Router from 'vue-router'
import tables from '@/components/tables'
import adduser from '@/components/adduser'
import addstreet from '@/components/AddStreet'
import addroute from '@/components/AddRoute'
import personsroutesview from '@/components/PersonsRoutesView'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/'
    },
    {
      path: '/tables',
      name: 'tables',
      component: tables
    },
    {
      path: '/adduser',
      name: 'adduser',
      component: adduser
    },
    {
      path: '/addstreet',
      name: 'addstreet',
      component: addstreet
    },
    {
      path: '/addroute',
      name: 'addroute',
      component: addroute
    },
    {
      path: '/personroutes',
      name: 'personroutes',
      component: personsroutesview
    }
  ]
})
