import '@/assets/css/tailwind.css'
import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import './registerServiceWorker'
import VueCookies from 'vue-cookies'
Vue.use(VueCookies)

// set default config
Vue.$cookies.config('7d')

Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
