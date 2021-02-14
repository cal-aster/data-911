import Vue from 'vue'
import VueMeta from 'vue-meta'
import Router from 'vue-router'
import { routes } from './routes'

Vue.use(Router)
Vue.use(VueMeta, {
  refreshOnceOnNavigation: true
})

const router = new Router({
  base: '/',
  mode: 'history',
  routes: routes
})

export default router