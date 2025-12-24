<template>
  <div class="home-layout">
    <BlogSidebar />
    <main class="home-content">
      <ArticleCard
        title="你好，世界"
        content="这是你的第一篇博客文章！你可以用 Markdown 来书写内容。"
      />
    </main>
  </div>
</template>

<script setup>
import BlogSidebar from '@/components/BlogSidebar.vue';
import ArticleCard from '@/components/ArticleCard.vue';
</script>

<style scoped>
.home-layout {
  display: flex;
}

.home-content {
  margin-left: 240px;
  padding: 2rem;
  flex: 1;
  min-height: 100vh;
}
</style>