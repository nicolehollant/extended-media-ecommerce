<template>
<div class="item" @click="viewItem" v-if="item !== null && !error">
  <div class="image">
    <img :src="publicPath + paths[0]">
    <div class="description">
      <p class="text-3xl">{{ name }}</p>
      <p class="text-xl">{{ date }}</p>
    </div>
  </div>
</div>

<div class="loading" v-else-if="item === null && !error">
  <div class="loading__copy">We're takin a look 🤠</div>
  <div class="loading__spinner" />
</div>

<div class="grid" v-else-if="error">
  There was an error loading our items 😢
</div>
</template>

<script>
import axios from 'axios';

import { publicPath, backendurl } from '@/conf'

export default {
  props: {
    name: {
      type: String,
      default: "item"
    },
    description: {
      type: String,
      default: "lorem ipsum sit dolor en aso"
    },
    date: {
      type: String,
      default: "11/12/2019"
    },
    paths: {
      type: null,
      default: ["/images/plupSmile.png"]
    },
    reviews: {
      type: null,
      default: () => {return [{user: "john", rating: 3, comment: "lorem ipsum"}]}
    }
  },
  data() {
    return {
      item: null,
      error: false,
      publicPath: publicPath, //process.env.BASE_URL
      // publicPath: "/extended-media-ecommerce", //process.env.BASE_URL
    }
  },
  methods: {
    viewItem() {
      this.$store.commit('setItem', { item: this.item })
      this.$router.push('/item')
    },
    loadItem() {
      console.log(this.name, this.$cookies.get('extended-media-item'), "")
      const name = this.name || this.$cookies.get('extended-media-item') || ""
      axios.get(backendurl + '/items/' + name).then(response => { 
        console.log(response); 
        if(response.status === 200) {
          const data = response.data.data;
          console.log(data)
          this.error = false
          this.item = data
        }
      })
      .catch(error => { 
        this.error = true
        console.log(error.response); 
      })
    }
  },
  mounted () {
    this.loadItem()
  },
}
</script>

<style lang="postcss" scoped>
.item {
  width: fit-content;
  @apply shadow rounded-2xl bg-gray-100 text-gray-700 flex-col-center;
}
img {
  width: 400px;
  height: 200px;
  object-fit: cover;
  @apply rounded ease;
}
.image {
  @apply relative;
}
.description {
  background-color: rgba(0, 0, 0, 0.55);
  overflow: scroll;
  @apply opacity-0 font-medium rounded text-gray-200 absolute top-0 left-0 right-0 bottom-0 p-2 ease flex-col-center text-3xl;
  /* @apply opacity-0 font-medium rounded text-gray-200 absolute top-0 left-0 right-0 bottom-0 p-2 ease; */
}
.item:hover .description {
  @apply opacity-100 ease-slow;
}
.item:hover img {
  filter: blur(2px) saturate(0.5) brightness(0.4);
}
h1 {
  @apply font-semibold text-xl leading-tight mt-2 mb-1;
}
.date {
  @apply font-medium;
}

.loading__copy {
  @apply text-xl font-medium text-green-800 mt-10;
}

.loading__spinner {
  @apply rounded-full w-24 h-24 border-green-700 border-t-4 my-8 mx-auto;
  border-width: 1rem;
  border-top: 1rem solid #81e6d9;
  animation: spin 2s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@media (min-width: 600px) {
img {
  height: 300px;
}
}

@media (min-width: 920px) {
img {
  height: 500px;
}
}
</style>