import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    redirect: '/onboarding'
  },
  {
    path: '/shop',
    name: 'shop',
    component: () => import('../views/Shop.vue')
  },
  {
    path: '/cart',
    name: 'cart',
    component: () => import('../views/Cart.vue')
  },
  {
    path: '/about',
    name: 'about',
    component: () => import('../views/About.vue')
  },
  {
    path: '/item',
    name: 'item',
    component: () => import('../views/Item.vue')
  },
  {
    path: '/onboarding',
    name: 'onboarding',
    component: () => import('../views/Onboarding.vue')
  },
  {
    path: '/account',
    name: 'account',
    component: () => import('../views/Account.vue')
  },
  {
    path: '/orders',
    name: 'orders',
    component: () => import('../views/Orders.vue')
  },
]

const router = new VueRouter({
  // mode: 'history',
  routes
})

export default router
