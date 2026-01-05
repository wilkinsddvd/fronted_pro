<script setup>
const props = defineProps(['post'])
</script>
<template>
  <article class="post-item">
    <h3>
      <router-link :to="{ name: 'PostDetail', params: { slug: post.id } }">{{ post.title }}</router-link>
    </h3>
    <div class="post-meta">
      <small class="date">{{ post.date }}</small>
      <span v-if="post.category" class="category">{{ post.category }}</span>
      <span v-if="post.author" class="author">作者: {{ post.author }}</span>
      <span class="views">浏览: {{ post.views || 0 }}</span>
    </div>
    <p>{{ post.summary }}</p>
    <div v-if="post.tags && post.tags.length" class="tags">
      <span v-for="tag in post.tags" :key="tag" class="tag">#{{ tag }}</span>
    </div>
  </article>
</template>
<style scoped>
.post-item { 
  border-bottom: 1px solid #eee; 
  margin-bottom: 1.5rem; 
  padding-bottom: 1rem;
}
h3 { 
  margin-bottom: 0.5rem;
}
h3 a {
  color: var(--color-text);
  text-decoration: none;
}
h3 a:hover {
  color: #007bff;
}
.post-meta {
  display: flex;
  gap: 1rem;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
  color: #666;
  flex-wrap: wrap;
}
.category {
  background: #e7f3ff;
  color: #0066cc;
  padding: 0.2rem 0.5rem;
  border-radius: 3px;
  font-size: 0.85rem;
}
.tags {
  display: flex;
  gap: 0.5rem;
  margin-top: 0.5rem;
}
.tag {
  color: #888;
  font-size: 0.85rem;
}
</style>