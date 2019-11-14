<template>
  <div id="app">
    <Navbar />
    <router-view/>
  </div>
</template>

<script>
import Navbar from '@/components/Navbar'
export default {
  components: {
    Navbar,
  },
}
</script>

<style lang='postcss'>
@import url("https://use.typekit.net/vxw4tlv.css");

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
