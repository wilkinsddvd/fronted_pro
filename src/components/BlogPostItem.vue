<script setup>
const props = defineProps(['post'])
</script>
<template>
  <article class="post-item">
    <h3>
      <router-link :to="'/post/' + post.slug">{{post.title}}</router-link>
    </h3>
    <small>{{post.date}}</small>
    <p>{{post.summary}}</p>
  </article>
</template>
<style scoped>
.post-item { border-bottom: 1px solid #eee; margin-bottom:1.5rem; padding-bottom:1rem;}
h3 { margin-bottom: .2rem;}
</style>