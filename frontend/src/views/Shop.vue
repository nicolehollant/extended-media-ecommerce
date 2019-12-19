<template>
  <div class="shop">
    <div class="grid" v-if="items !== null && !error">
      <div v-for="item in items" :key="item.id">
        <ShopItem 
          :name="item.name"
          :description="item.description"
          :date="item.date"
          :paths="getPaths(item.paths)"
        />
          <!-- :reviews="item.reviews" -->
      </div>
    </div>

    <div class="loading" v-if="items === null && !error">
      <div class="loading__copy">We're on the hunt for those items 🤙</div>
      <div class="loading__spinner" />
    </div>

    <div class="grid" v-if="error">
      There was an error loading our items 😢
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import ShopItem from '@/components/ShopItem'

import { backendurl } from '@/conf'

export default {
  components: {
    ShopItem,
  },
  data() {
    return {
      items: null,
      error: false,
      // items: require("@/assets/items.json")["items"]
    }
  },
  methods: {
    getPaths(paths) {
      // return paths.map(e => `/images/${e}`)
      return paths
    },
    loadItems() {
      axios.get(backendurl + '/items/').then(response => { 
        console.log(response); 
        if(response.status === 200) {
          const data = response.data.data;
          this.error = false
          this.items = data
        }
      })
      .catch(error => { 
        this.error = true
        console.log(error.response); 
      })
    }
  },
  mounted () {
    this.loadItems();
  },
}
</script>

<style scoped lang="postcss">
.shop {
  --item-width: 400px;
  --num-columns: 2;
  --grid-gap: 0.25rem;
  padding: 1rem;
  @apply mt-4;
}
.grid {
  max-width: calc(var(--num-columns) * var(--item-width) + ((var(--num-columns) - 1) * var(--grid-gap)));
  display: grid;
  grid-template-columns: repeat(var(--num-columns), 1fr);
  /* grid-template-columns: repeat(1, 1fr); */
  grid-gap: var(--grid-gap);
  @apply my-4 mx-auto;
}
.grid-item {
  @apply flex-center;
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
.shop {
  --num-columns: 3;
}
}
</style>