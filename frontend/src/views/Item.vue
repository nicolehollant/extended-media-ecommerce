<template>
<div class="item-view" v-if="Object.keys(item).length > 0">
  <div class="add-review__modal--wrapper" v-if="modalUp">
    <div class="add-review__modal--clicklayer" @click="dismissModal"/>
    <div class="add-review__modal">
      <h1>Add a Review</h1>
      <p class="font-semibold mb-1 text-left text-sm capitalize text-gray-700">rating:</p>
      <div class="form-stars">
        <div 
          v-for="(_, index) in Array(5)" 
          :key="`star-${index}`"
          @click="() => currentRating = index"
        >
            <svg class="form-star form-star--filled" v-if="index <= currentRating" width="116" height="111" viewBox="0 0 116 111" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M58.4615 2.01645L73.0726 37.15C73.5766 38.362 74.7164 39.19 76.0248 39.2949L113.954 42.334C114.397 42.3695 114.577 42.9228 114.239 43.2122L85.3403 67.965C84.3434 68.8189 83.908 70.1587 84.2126 71.4355L93.043 108.447C93.1462 108.88 92.6755 109.222 92.296 108.99L59.8243 89.1546C58.7042 88.4704 57.2954 88.4704 56.1753 89.1546L23.7036 108.99C23.3241 109.222 22.8534 108.88 22.9567 108.447L31.787 71.4355C32.0916 70.1587 31.6562 68.8189 30.6594 67.965L1.76046 43.2121C1.42267 42.9228 1.60243 42.3695 2.04579 42.334L39.9749 39.2949C41.2833 39.19 42.423 38.3619 42.927 37.15L57.5382 2.01644C57.7089 1.60578 58.2907 1.60577 58.4615 2.01645Z" stroke="black" stroke-width="3"/>
            </svg>
            <svg class="form-star" v-else width="116" height="111" viewBox="0 0 116 111" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M58.4615 2.01645L73.0726 37.15C73.5766 38.362 74.7164 39.19 76.0248 39.2949L113.954 42.334C114.397 42.3695 114.577 42.9228 114.239 43.2122L85.3403 67.965C84.3434 68.8189 83.908 70.1587 84.2126 71.4355L93.043 108.447C93.1462 108.88 92.6755 109.222 92.296 108.99L59.8243 89.1546C58.7042 88.4704 57.2954 88.4704 56.1753 89.1546L23.7036 108.99C23.3241 109.222 22.8534 108.88 22.9567 108.447L31.787 71.4355C32.0916 70.1587 31.6562 68.8189 30.6594 67.965L1.76046 43.2121C1.42267 42.9228 1.60243 42.3695 2.04579 42.334L39.9749 39.2949C41.2833 39.19 42.423 38.3619 42.927 37.15L57.5382 2.01644C57.7089 1.60578 58.2907 1.60577 58.4615 2.01645Z" stroke="black" stroke-width="3"/>
            </svg>
        </div>
      </div>

      <FormTextarea 
        class="onboarding__form--input"
        name="comment"
        placeholder="comment"
        label="comment"
        :value="comment"
        :error="commentError"
        @input="e => comment = e"
      /> 

      <button class="add-review__modal--submit" @click="addReview">Submit</button>

    </div>
  </div>
  <div class="preview" :class="{'preview--blur': modalUp}">
    <div class="active-item">
      <video controls class="image" v-if="isVideo(item.paths[imgIndex])">
        <source :src="publicPath + item.paths[imgIndex]">
        This video isnt supported
      </video>
      <img :src="publicPath + item.paths[imgIndex]" class="image" v-else>
    </div>
    <div class="active-controls">
      <button class="active-control-button" @click="previous">&larr;</button>
      <button class="active-control-button" @click="next">&rarr;</button>
    </div>
    <div class="image-preview-container">
      <div 
        v-for="(path, index) of item.paths" 
        :key="`path-${index}`"  
        class="other-image-container"
        :class="{'pl-0 pr-2': index === 0, 'pl-2 pr-0': index === item.paths.length - 1 }"
      >
        <video 
          :src="publicPath + item.paths[index]" 
          @click="imgIndex = index"
          class="other-image"
          v-if="isVideo(item.paths[index])"
        >This video isnt supported</video>
        <img 
          :src="publicPath + item.paths[index]" 
          @click="imgIndex = index"
          class="other-image"
          v-else
        >
      </div>
    </div>
  </div>
  <div class="info-wrapper" :class="{'preview--blur': modalUp}">
    <div class="info">
      <h1 class="name">{{item.name}}</h1>
      <p class="date">{{item.date}}</p>
      <p class="description">{{item.description}}</p>
    </div>

    <button class="add-to-cart" @click="addToCart">Add To Cart</button>
    

    <div class="reviews">
      <div class="stars">
        <img class="star" src="@/assets/starFilled.svg" v-for="(_, index) in Array(parseInt(rating))" :key="`overall-filled-${index}`">
        <img class="star" src="@/assets/starEmpty.svg" v-for="(_, index) in Array(5 - parseInt(rating))" :key="`overall-empty-${index}`">
      </div>

      <button class="add-review" @click="raiseModal">Write A Review</button>

      <div class="reviews-header">
        <div class="reviews-header-line"></div>
        <h2 class="reviews-header-text">Reviews</h2>
        <div class="reviews-header-line"></div>
      </div>
      <div class="reviews-body">
        <Review
          v-for="(review, index) of item.reviews" 
          :key="`review-${index}`" 
          :review="review" 
          class="review"
        />
      </div>
    </div>

  </div>
  <!-- <p>{{item}}</p> -->
</div>
<div v-else>
  Error loading item
</div>
</template>

<script>
import axios from 'axios';
import Review from '@/components/Review.vue'
import { mapGetters } from 'vuex'
import { DateTime } from 'luxon'
import FormTextarea from '@/components/ui/FormTextarea'

import { publicPath, backendurl } from '@/conf'

export default {
  components: {
    Review,
    FormTextarea
  },
  computed: {
    ...mapGetters([
      'currentItem',
      'user'
    ]),
    rating() {
      let num = 0;
      for(const review of this.item.reviews) {
        num += review.rating
      }
      return Math.round(num / this.item.reviews.length)
    }
  },
  data() {
    return {
      comment: '',
      commentError: '',
      currentRating: 2,
      modalUp: false,
      item: {},
      imgIndex: 0,
      publicPath: publicPath, //process.env.BASE_URL
      // publicPath: "/extended-media-ecommerce", //process.env.BASE_URL
    }
  },
  methods: {
    isVideo(src) {
      return (src.endsWith(".MOV") || src.endsWith(".mp4"));
    },
    previous() {
      this.imgIndex--
      if(this.imgIndex < 0) this.imgIndex = this.item.paths.length - 1
    },
    next() {
      this.imgIndex++
      if(this.imgIndex > this.item.paths.length - 1) this.imgIndex = 0
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
    raiseModal() {
      this.modalUp = true;
    },
    dismissModal() {
      this.modalUp = false;
    },
    addToCart() {
      this.$store.commit('addItem', { item: this.item })
    },
    addReview() {
      this.requestError = ''
      let error = false;
      if(this.comment.length < 1) {
        this.commentError = "comment must be > 1 characters"
        error = true;
      } else { this.commentError = "" }
      if (error) return;
      const date = DateTime.local().toSQL()
      const data = {
        name: this.item.name,
        password: this.user.password,
        email: this.user.email,
        rating: this.currentRating + 1,
        comment: this.comment,
        date: date
      }
      axios.put(backendurl + '/items/review/', data).then(response => { 
        console.log(response); 
        if(response.status === 201) {
          const data2 = response.data.data;
          console.log(data2)
          setTimeout(() => {
            this.loadItem(this.item.name)
            this.dismissModal()
          }, 300);
        }
      })
      .catch(error => { 
        this.requestError = error.response.data.message || error.response.data || error.response || error;
        console.log(error.response); 
      });
    },
    loadItem(name) {
      axios.get(backendurl + '/items/' + name).then(response => { 
        if(response.status === 200) {
          const data = response.data.data;
          this.$store.commit('setItem', { item: data })
          this.item = data
        }
      })
      .catch(error => { 
        console.log(error.response); 
      })
    },
  },
  mounted () {
    this.item = this.currentItem || {}
    if(Object.keys(this.item).length === 0) {
      let cookie = this.$cookies.get('extended-media-item') || ""
      this.loadItem(cookie)
    }
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

.add-review {
  @apply block mt-8 font-bold text-lg text-teal-600 mx-auto
}

.add-review__modal--wrapper {
  @apply fixed top-0 left-0 w-screen h-screen flex-center z-modal-behind;
}
.add-review__modal--clicklayer {
  background: #00000060;
  @apply absolute top-0 left-0 right-0 bottom-0 z-modal
}
.add-review__modal {
  @apply w-full mx-8 bg-gray-100 rounded-lg z-modal-front px-8 py-4;
}
.preview--blur {
  filter: blur(3px);
}
.add-review__modal h1 {
  @apply capitalize text-green-800 font-medium text-2xl leading-loose my-3;
}
.add-review__modal--submit {
  @apply relative px-8 py-2 mt-8 mb-4 border-2 border-green-500 font-semibold rounded-full ease;
}
.add-review__modal--submit:hover {
  @apply bg-green-300;
}
.add-review__modal--submit:focus {
  outline: none;
  @apply bg-teal-200;
}

.form-stars {
  width: fit-content;
  @apply flex items-center mb-4 py-2 border-2 border-transparent bg-transparent mx-auto;
}
.form-star {
  fill: #f7fafc;
  @apply w-5 h-5 m-1 cursor-pointer ease;
}
.form-star--filled {
  fill: black;
}
.form-star:hover {
  fill: #38a169;
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
.add-review__modal {
  @apply max-w-lg w-full bg-gray-100 rounded-lg z-modal-front px-8 py-4;
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