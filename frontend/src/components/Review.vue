<template>
<div class="review">
  <div class="left">
    <img src="@/assets/account.svg" class="account">
    <div class="stars">
      <img class="star" src="@/assets/starFilled.svg" v-for="x in Array(review.rating)" :key="`filled-${x}`">
      <img class="star" src="@/assets/starEmpty.svg" v-for="x in Array(5 - review.rating)" :key="`empty-${x}`">
    </div>
  </div>
  <div class="content">
    <div class="name">{{review.user}}</div>
    <div class="comment">{{review.comment}}</div>
  </div>

</div>
</template>

<script>
export default {
  props: {
    review: {
      type: null,
      default: () => {
        return {
          user: "Jim",
          rating: 4,
          comment: "This sure is cool"
        }
      }
    },
  }
}
</script>

<style lang="postcss" scoped>
.review {
  justify-content: space-evenly;
  @apply flex items-start;
}
.account {
  @apply w-10 h-10 rounded-full border-2 border-black mx-auto mb-1;
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
@media (min-width: 920px) {

}

@media (min-width: 1240px) {
.content {
  width: 300px;
  @apply text-left;
}
}
</style>