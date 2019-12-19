import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    item: {},
    cart: [],
    user: {}
  },
  getters: {
    currentItem: state => state.item,
    cart: state => state.cart,
    user: state => state.user,
    avatar: state => {
      let avatarNum = state.user.avatar || 0
      return `/avatars/avatar${avatarNum  + 1}.png`
    },
  },
  mutations: {
    setUser (state, payload) {
      state.user = payload.user
      Vue.$cookies.set('extended-media-user', JSON.stringify(payload.user))
    },
    setItem (state, payload) {
      state.item = payload.item
      Vue.$cookies.set('extended-media-item', payload.item.name)
    },
    addItem (state, payload) {
      if(state.cart.find(e => e.name === payload.item.name)) return
      state.cart.push(payload.item)
    },
    removeItem (state, payload) {
      state.cart.splice(state.cart.indexOf(payload.item), 1)
    },
  },
  actions: {
  },
  modules: {
  }
})
