import Vue from 'vue'
import Meta from 'vue-meta'
import Router from 'vue-router'
import { routes } from './routes'

Vue.use(Router)

const router = new Router({
  base: '/',
  mode: 'history',
  routes: routes
})

Vue.use(Meta)

export default router