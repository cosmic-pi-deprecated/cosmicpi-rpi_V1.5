import Vue from 'vue'
import Router from 'vue-router'
import Dashboard from './components/dashboard/Dashboard.vue'
import About from './components/About.vue'
import Settings from './components/settings/Settings.vue'
import Science from './components/Science.vue'


Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      components: {
        main: Dashboard
      }
    },
    {
      path: '/about',
      components: {
        main: About
      }
    },
    {
      path: '/settings',
      components: {
        main: Settings
      }
    },
    {
      path: '/science',
      components: {
        main: Science
      }
    },
  ]
})
