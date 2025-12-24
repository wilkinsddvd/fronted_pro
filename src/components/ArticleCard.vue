<template>
  <div class="article-card">
    <h2>{{ title }}</h2>
    <p>{{ content }}</p>
  </div>
</template>

<script setup>
defineProps({
  title: String,
  content: String,
});
</script>

<style scoped>
.article-card {
  background: rgba(46, 48, 51, 0.96);
  border-radius: 18px;
  box-shadow: 0 8px 38px 0 rgba(44, 240, 214, 0.08), 0 6px 36px rgba(30,30,30,0.22);
  padding: 2.6rem 2.3rem;
  margin: 2rem auto;
  max-width: 800px;
}
.article-card h2 {
  color: #caeff1;
  margin-bottom: 1rem;
}
.article-card p {
  color: #e6f3ea;
  line-height: 1.78;
}
</style>