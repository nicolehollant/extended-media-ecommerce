<template>
<div class="item-view">
  <div class="preview">

    <div class="active-item">
      <video controls class="image" v-if="isVideo(currentItem.paths[imgIndex])">
        <source :src="publicPath + currentItem.paths[imgIndex]">
        This video isnt supported
      </video>
      <img :src="publicPath + currentItem.paths[imgIndex]" class="image" v-else>
    </div>
    <div class="active-controls">
      <button class="active-control-button" @click="previous">&larr;</button>
      <button class="active-control-button" @click="next">&rarr;</button>
    </div>
    <div class="image-preview-container">
      <div 
        v-for="(path, index) of currentItem.paths" 
        :key="`path-${index}`"  
        class="other-image-container"
        :class="{'pl-0 pr-2': index === 0, 'pl-2 pr-0': index === currentItem.paths.length - 1 }"
      >
        <video 
          :src="publicPath + currentItem.paths[index]" 
          @click="imgIndex = index"
          class="other-image"
          v-if="isVideo(currentItem.paths[index])"
        >This video isnt supported</video>
        <img 
          :src="publicPath + currentItem.paths[index]" 
          @click="imgIndex = index"
          class="other-image"
          v-else
        >
      </div>
    </div>
  </div>
  <div class="info-wrapper">
    <div class="info">
      <h1 class="name">{{currentItem.name}}</h1>
      <p class="date">{{currentItem.date}}</p>
      <p class="description">{{currentItem.description}}</p>
    </div>

    <button class="add-to-cart" @click="addToCart">Add To Cart</button>

    <div class="reviews">
      <div class="stars">
        <img class="star" src="@/assets/starFilled.svg" v-for="x in Array(rating)" :key="`filled-${x}`">
        <img class="star" src="@/assets/starEmpty.svg" v-for="x in Array(5 - rating)" :key="`empty-${x}`">
      </div>
      <div class="reviews-header">
        <div class="reviews-header-line"></div>
        <h2 class="reviews-header-text">Reviews</h2>
        <div class="reviews-header-line"></div>
      </div>
      <div class="reviews-body">
        <Review
          v-for="(review, index) of currentItem.reviews" 
          :key="`review-${index}`" 
          :review="review" 
          class="review"
        />
      </div>
    </div>
  </div>
  <!-- <p>{{currentItem}}</p> -->
</div>
</template>

<script>
import Review from '@/components/Review.vue'

import { mapGetters } from 'vuex'
export default {
  components: {
    Review
  },
  computed: {
    ...mapGetters([
      'currentItem',
    ]),
    rating() {
      let num = 0;
      for(const review of this.currentItem.reviews) {
        num += review.rating
      }
      return Math.round(num / this.currentItem.reviews.length)
    }
  },
  data() {
    return {
      imgIndex: 0,
      publicPath: "/extended-media-ecommerce", //process.env.BASE_URL
    }
  },
  methods: {
    isVideo(src) {
      return (src.endsWith(".MOV") || src.endsWith(".mp4"));
    },
    previous() {
      this.imgIndex--
      if(this.imgIndex < 0) this.imgIndex = this.currentItem.paths.length - 1
    },
    next() {
      this.imgIndex++
      if(this.imgIndex > this.currentItem.paths.length - 1) this.imgIndex = 0
    },
    navigate(e) {
      if ( e.keyCode == '37') {
        e.preventDefault()
        this.previous();
      }
      else if (e.keyCode == '39') {
        e.preventDefault()
        this.next();
      }
    },
    addToCart() {
      this.$store.commit('addItem', { item: this.currentItem })
    }
  },
  mounted () {
    window.addEventListener('keydown', this.navigate);
  },
  beforeDestroy () {
    window.removeEventListener('keydown', this.navigate);
  },
}
</script>

<style lang="postcss" scoped>
.item-view {
  max-width: 1450px;
  @apply p-4 mx-auto flex flex-col justify-center h-full mt-8;
}
.image {
  width: 100%;
  max-width: 100%;
  max-height: 80vh;
  object-fit: contain;
  @apply rounded mb-8 mx-auto;
}
.info-wrapper {
  @apply font-medium px-4;
}
.info {
  width: 300px;
  max-width: calc(100% - 1rem);
  @apply my-8 mx-auto;
}
.name {
  @apply font-semibold text-3xl
}
.date {
  @apply font-semibold text-gray-600 text-xl;
}
.description {
  @apply mt-4 text-lg leading-loose;
}
.other-image-container {
  /* width: 1fr; */
  @apply p-1;
}
.other-image {
  width: 80px;
  height: 80px;
  object-fit: cover;
  @apply rounded cursor-pointer shadow ease;
}
.other-image:hover {
  filter: saturate(0.4) brightness(0.4);
  @apply shadow-xl;
}
.image-preview-container {
  flex-wrap: wrap;
  justify-content: center;
  @apply flex;
}
.active-item {
  @apply relative;
}
.active-controls {
  /* @apply absolute top-0 bottom-0 left-0 right-0 flex items-center justify-between; */
  @apply w-12 h-12 flex items-center justify-between mx-auto mb-8;
}
.active-control-button {
  opacity: 50%;
  @apply block w-8 h-8 bg-gray-800 rounded text-gray-100 font-bold text-xl -m-4 ease;
}
.active-control-button:hover {
  opacity: 90%;
}
.active-control-button:focus {
  outline: none;
}

.stars {
  width: fit-content;
  @apply flex mx-auto mt-20;
}
.star {
  @apply w-8 h-8 m-1;
}

.reviews-header {
  @apply flex items-center mx-4 mt-8;
}
.reviews-header-text {
  @apply font-semibold text-xl;
}
.reviews-header-line {
  width: 100%;
  height: 2px;
  @apply bg-gray-600 mx-4;
}
.review {
  @apply  my-16;
}
.review:first-of-type {
  @apply mt-8;
}
.add-to-cart {
  @apply relative px-4 py-2 border-2 border-green-500 font-semibold rounded-full ease;
}
.add-to-cart:hover {
  @apply bg-green-300;
}
.add-to-cart:focus {
  outline: none;
}
.add-to-cart:hover:focus::after {
  content: "Success!!";
  position: absolute;
  top: calc(100% + 0.5rem);
  left: 0;
  right: 0;
}




@media (min-width: 920px) {
  .info-wrapper {
  width: 40%;
}
  .preview {
  max-width: 60%;
  @apply ml-4;
}
  .item-view {
  max-width: 1450px;
  @apply p-4 mx-auto flex flex-row justify-center h-full mt-8;
}
.image {
  width: 500px;
  max-width: 500px;
  max-height: 80vh;
  object-fit: contain;
  @apply rounded mb-8 mx-auto;
}
.info-wrapper {
  width: 40%;
  @apply font-medium px-4;
}
.info {
  width: 300px;
  @apply my-8 mx-auto;
}
}





@media (min-width: 1240px) {
.image {
  width: 700px;
  max-width: 700px;
  max-height: 80vh;
  object-fit: contain;
  @apply rounded mb-8 mx-auto;
}
.info-wrapper {
  width: 40%;
  @apply font-medium px-4;
}
.info {
  width: 400px;
  @apply my-8 mx-auto;
}
.other-image {
  width: 140px;
  height: 140px;
  object-fit: cover;
  @apply rounded cursor-pointer shadow ease;
}

}
</style>