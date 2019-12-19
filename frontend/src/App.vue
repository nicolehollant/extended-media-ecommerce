<template>
  <div id="app">
    <Navbar />
    <router-view/>
  </div>
</template>

<script>
import Navbar from '@/components/Navbar'
import { mapGetters } from 'vuex'

export default {
  components: {
    Navbar
  },
  computed: {
    ...mapGetters([
      'user',
    ])
  },
  mounted() {
    if(Object.keys(this.user).length === 0) {
      let cookie = this.$cookies.get('extended-media-user') || {}
      this.$store.commit('setUser', { user: cookie })
      if(Object.keys(cookie).length === 0) this.$router.push("onboarding")
    }
  }
}
</script>

<style lang='postcss'>
@import url("https://use.typekit.net/vxw4tlv.css");
html {
  @apply bg-gray-100
}
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  /* font-family: futura-pt, Helvetica, Arial, sans-serif; */
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  @apply relative bg-gray-100 min-h-screen;
}

#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>
