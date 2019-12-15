<template>
  <div class="about">
    <div class="title">Extended Media</div>
    <div class="subtitle">Project Three</div>

    <p>This is a project centered around memory / preservation. The idea here was fairly vague, I had wanted to take memories that were dear to me and plaster them on some sort of e-commerce site. These portals are often rather invasive or at the very least public, which interacts in a weird, kind of uncomfortable way with things like pictures of one's family.</p>
    <p>I've never been the type to be concerned about the state of surveillance or data collection, but this paints a certain picture of the marketing of ourselves through the use of platforms like facebook and whatnot. Again, it's not something I'm perturbed by, but it can be nice to think about what you're putting out there.</p>
    <p>Mostly, I thought this was a fun project. It was a nice change of pace going an e-commerce route, and I had never done something like this before. It was nice trying to think of little mock reviews, and there was a pleasant aspect to the gathering of these memories.</p>
    <p>I hope you enjoy, and I'm sorry about the lack of responsiveness for this page. Hard to deal with that under tight time constraints :shrug:</p>
  </div>
</template>

<style lang="postcss" scoped>
.about {
  max-width: calc(100vw - 2rem);
  @apply mx-auto;
}
.title {
  @apply text-3xl font-bold mt-8 mb-4;
}
.subtitle {
  @apply text-2xl font-semibold mb-4;
}
p {
  @apply font-medium text-lg text-left mb-4 leading-loose;
}
@media (min-width: 800px) {
.about {
  max-width: calc(100vw - 6rem);
  @apply max-w-3xl mx-auto;
}
}
</style>
