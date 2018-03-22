import Vue from 'vue'
import Router from 'vue-router'
import Dashboard from './components/Dashboard.vue'
import About from './components/About.vue'

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
  ]
})
