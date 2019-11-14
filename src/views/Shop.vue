<template>
  <div class="shop">
    <div class="grid">
      <div v-for="item in items" :key="item.id">
        <ShopItem 
          :name="item.name"
          :description="item.description"
          :date="item.date"
          :paths="getPaths(item.paths)"
          :reviews="item.reviews"
        />
      </div>
    </div>
  </div>
</template>

<script>
import ShopItem from '@/components/ShopItem'
export default {
  components: {
    ShopItem,
  },
  data() {
    return {
      items: require("@/assets/items.json")["items"]
    }
  },
  methods: {
    getPaths(paths) {
      // return paths.map(e => `/images/${e}`)
      return paths
    }
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


@media (min-width: 600px) {
.shop {
  --num-columns: 3;
}
}
</style>