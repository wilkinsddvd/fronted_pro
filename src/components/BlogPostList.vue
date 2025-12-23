<script setup>
import { ref, onMounted } from 'vue'
import BlogPostItem from './BlogPostItem.vue'

// 手动维护或者自动生成的文章列表
const posts = ref([
  { title: '你好，世界', slug: 'hello-world', summary: '第一篇示例文章', date: '2025-12-23' },
  // 可拓展
])
</script>
<template>
  <section>
    <h2>文章列表</h2>
    <BlogPostItem v-for="post in posts" :key="post.slug" :post="post"/>
  </section>
</template>