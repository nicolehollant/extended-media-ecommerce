import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
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
  }
]

const router = new VueRouter({
  // mode: 'history',
  routes
})

export default router
