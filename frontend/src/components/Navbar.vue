<template>
  <div class="navbar">
    <div class="nav-content">
      <div class="logo"><img src="@/assets/logo.svg"></div>
      <!-- <div class="nav"> -->
        <div class="navbar--links">
          <router-link class="navbar--links__link" v-for="link in links" :key="link.name" :to="link.to">
            {{ link.name }}
          </router-link>
        </div>
      <!-- </div> -->

      <!-- <button class="account"><img src="@/assets/accountTransparent.svg"></button> -->
      <button class="account" @click="() => navigate('account')"><img :src="publicPath + avatar" ></button>
      <button class="hamburger" @click="navUp = !navUp"><img class="block" src="@/assets/hamburger.svg">
        <div class="mobile-nav" v-if="navUp">
          <li class="mobile-nav--link" v-for="link in links" :key="link.name" @click="() => navigate(link.to)">
            {{ link.name }}
          </li>
        </div>
      </button>
    </div>
  </div>
</template>

<script>
const link = (name, to) => {
  return {
    name: name,
    to: to
  }
}
import { mapGetters } from 'vuex'
import { publicPath } from '@/conf'

export default {
  computed: {
    ...mapGetters([
      'avatar'
    ])
  },
  data() {
    return {
      links: [
        link("Shop", "/shop"),
        link("Cart", "/cart"),
        link("About", "/about"),
      ],
      navUp: false,
      publicPath: publicPath, //process.env.BASE_URL
      // publicPath: "/extended-media-ecommerce", //process.env.BASE_URL
    }
  },
  methods: {
    raiseNav() {
      this.navUp = true;
    },
    navigate(to) {
      setTimeout(() => {
      this.navUp = false;
      });
      this.$router.push(to)
    }
  },
}
</script>

<style scoped lang="postcss">
.navbar {
  @apply relative bg-green-300 p-8 z-nav shadow-lg;
}
.nav-content {
  max-width: 1200px;
  margin: auto;
  position: relative;
  @apply flex items-center;
}
.navbar--links {
  max-width: 450px;
  @apply hidden w-full justify-around mx-auto pl-12;
}
.navbar--links__link {
  @apply text-teal-600 font-semibold ease relative;
}
.navbar--links__link:hover {
  @apply text-teal-800;
}
.navbar--links__link::after {
  content: "";
  left: -0.5rem;
  height: 2px;
  bottom: -0.125rem;
  @apply absolute block bg-teal-800 w-0 ease;
}
.navbar--links__link:hover::after {
  width: calc(100% + 1rem);
}
.navbar--links__link.router-link-exact-active {
  @apply text-teal-900;
}
.logo {
  @apply absolute top-0 bottom-0 flex items-center;
}
.account {
  right: 2rem;
  @apply w-12 flex items-center bg-green-100 border-2 border-black rounded-full ml-auto mr-4 ease;
}
.account:hover {
  @apply bg-green-900 shadow-lg
}
.account:focus {
  outline: none;
}
.account:hover img {
  transform: rotate(-15deg)
}
.account img {
  @apply rounded-full ease-slow
}
.hamburger {
  @apply relative w-6 top-0 bottom-0 right-0 flex items-center
}
.hamburger:focus {
  outline: none;
}
.mobile-nav {
  top: 2rem;
  right: -1rem;
  width: fit-content;
  list-style: none;
  @apply absolute bg-gray-200 px-8 py-4 rounded-xl shadow-xl border border-teal-600;
}
.mobile-nav--link {
  @apply p-2 font-medium text-teal-600 ease;
}
.mobile-nav--link:hover {
  @apply text-teal-800 underline
}
@media (min-width: 850px) {
.logo {
  left: 2rem;
}
.navbar--links {
  @apply flex;
}
.account {
  @apply flex ml-0;
}
.hamburger {
  @apply hidden;
}
.mobile-nav {
  @apply hidden;
}
}
</style>