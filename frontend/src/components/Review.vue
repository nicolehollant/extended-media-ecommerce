<template>
<div class="review">
  <div class="left">
    <img class="account" :src="avatar" >
    <div class="stars">
      <img class="star" src="@/assets/starFilled.svg" v-for="(_, index) in Array(parseInt(review.rating))" :key="`${review.username}-filled-${index}`">
      <img class="star" src="@/assets/starEmpty.svg" v-for="(_, index) in Array(5 - parseInt(review.rating))" :key="`${review.username}-empty-${index}`">
    </div>
  </div>

  <div class="content">
    <div class="name">{{review.username}}</div>
    <div class="date">{{date}}</div>
    <div class="comment">{{review.comment}}</div>
  </div>

</div>
</template>

<script>
import { DateTime } from 'luxon';
import { publicPath } from '@/conf'

export default {
  props: {
    review: {
      type: null,
      default: () => {
        return {
          username: "Jim",
          avatar: 2,
          date: Date.now().toLocaleString(),
          rating: 4,
          comment: "This sure is cool"
        }
      }
    },
  },
  data() {
    return {
      publicPath: publicPath, //process.env.BASE_URL
      // publicPath: "/extended-media-ecommerce", //process.env.BASE_URL
    }
  },
  computed: {
    avatar() {
      let avatarNum = this.review.avatar || 0
      return this.publicPath + `/avatars/avatar${avatarNum  + 1}.png`
    },
    date() {
      const res = DateTime.fromSQL(this.review.date).toLocaleString(DateTime.DATE_FULL) || this.review.date
      if (res == "Invalid DateTime") {
        return this.review.date
      }
      return res
    }
  },
}
</script>

<style lang="postcss" scoped>
.review {
  justify-content: space-evenly;
  @apply flex items-start;
}
.account {
  @apply w-12 h-12 rounded-full border-2 border-black mx-auto mb-1;
}
.stars {
  @apply flex;
}
.star {
  @apply w-4 h-4;
}
.content {
  width: 200px;
  @apply text-left;
}
.name {
  @apply font-bold mb-1;
}
.date {
  @apply leading-tight text-xs font-semibold text-gray-600 mb-1
}
@media (min-width: 920px) {

}

@media (min-width: 1240px) {
.content {
  width: 300px;
  @apply text-left;
}
}
</style>