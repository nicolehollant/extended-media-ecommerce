<template>
<div class="item" @click="viewItem">
  <div class="image">
    <img :src="paths[0]">
    <!-- <p class="description">{{ description }}</p> -->
    <div class="description">
      <p class="text-3xl">{{ name }}</p>
      <p class="text-xl">{{ date }}</p>
    </div>
  </div>
  <!-- <h1>{{ name }}</h1> -->
  <!-- <p class="date">{{ date }}</p> -->
</div>
</template>

<script>
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
      default: {user: "john", rating: 3, comment: "lorem ipsum"}
    }
  },
  data() {
    return {
      item: null
    }
  },
  methods: {
    viewItem() {
      this.$store.commit('setItem', { item: this.item })
      this.$router.push('/item')
    }
  },
  mounted () {
    this.item = {
      name: this.name,
      description: this.description,
      date: this.date,
      paths: this.paths,
      reviews: this.reviews
    };
  },
}
</script>

<style lang="postcss" scoped>
.item {
  width: fit-content;
  @apply shadow rounded-2xl bg-gray-100 text-gray-700 flex-col-center;
  /* max-width: 500px;
  @apply w-full p-4 shadow rounded-2xl bg-gray-100 text-gray-700 flex-col-center; */
}
img {
  width: 400px;
  height: 500px;
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
</style>