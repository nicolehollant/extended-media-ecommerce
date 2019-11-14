import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    item: { 
      name: "Microwave Computer", 
      description: "Hunter and I built a computer in a microwave! It was good fun, we enlisted my buddy to do some metal work—he cut the hole for the IO shield—and we payed him by letting him keep all the innards. Perhaps he's on a government watch list now, but you never know!", 
      date: "Feb 2, 2018", 
      paths: [ "/images/microwave1.JPG", "/images/microwave2.JPG", "/images/microwave3.JPG" ] 
    },
    cart: []
  },
  getters: {
    currentItem: state => {
      return state.item
    },
    cart: state => {
      return state.cart
    }
  },
  mutations: {
    setItem (state, payload) {
      state.item = payload.item
    },
    addItem (state, payload) {
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
