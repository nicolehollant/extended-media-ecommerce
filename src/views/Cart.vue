<template>
<div class="cart">
  <h1>My Cart</h1>
  <div v-if="$store.getters.cart.length > 0">
    <div class="table-wrapper">
      <table>
        <tr v-for="(item, index) in $store.getters.cart" :key="`item-${item.name}-${index}`">
          <td><img :src="'/extended-media-ecommerce/' + item.paths[0]" class="preview"></td>
          <td><p class="name">{{ item.name }}</p></td>
          <td><p class="date">{{ item.date }}</p></td>
          <button class="remove" @click="() => remove(item)">&times;</button>
        </tr>
      </table>
    </div>
    <button class="submit">Checkout</button>
  </div>
  <div v-else>
    <h3 class="text-xl font-medium">Sorry, cart is empty right now!</h3>
  </div>
</div>
</template>

<script>
export default {
  methods: {
    remove(item) {
      this.$store.commit('removeItem', {item: item})
    }
  },
}
</script>

<style scoped lang="postcss">
.cart {
  margin: auto;
}
h1 {
  @apply text-3xl font-semibold my-8;
}
table {
  max-width: calc(100vw - 6rem);
  position: relative;
}
.table-wrapper {
  width: max-content;
  @apply bg-gray-200 p-4 m-auto;
}
tr:nth-child(even) {
  @apply bg-gray-200 p-2;
}
tr:nth-child(odd) {
  @apply bg-gray-100 p-2;
}
.preview {
  @apply w-20 h-20 mr-2 rounded p-2;
}
.name, .date {
  @apply font-semibold mx-2;
}
.name {
  @apply capitalize text-left;
}
.date {
  @apply text-right;
}
.remove {
  left: calc(100% + 1.5rem);
  height: 5rem;
  @apply absolute font-black text-2xl;
}
.submit {
  @apply relative px-4 py-2 border-2 border-green-500 font-semibold rounded-full ease mt-8;
}
.submit:hover {
  @apply bg-green-300;
}
.submit:focus {
  outline: none;
}
@media (min-width: 600px) {
.preview {
  @apply w-20 h-20 mr-12 rounded p-2;
}
.name, .date {
  @apply font-semibold mx-12;
}
}

@media (min-width: 920px) {
table {
  max-width: 800px;
  position: relative;
}
.remove {
  left: calc(100% + 3rem);
  height: 5rem;
  @apply absolute font-black text-2xl;
}
}
</style>