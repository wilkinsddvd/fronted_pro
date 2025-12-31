<template>
  <div class="blog-main">
    <h2 class="blog-title">文章列表</h2>
    <div v-for="post in filteredPosts" :key="post.id" class="post-card">
      <div class="post-header">
        <h3 class="post-title">{{ post.title }}</h3>
        <span class="post-date">{{ post.date }}</span>
      </div>
      <div class="post-content">{{ post.content }}</div>
      <div class="post-divider"/>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { ref } from 'vue'
const props = defineProps({
  search: String,
  date: String
})

const posts = ref([
  { id: 1, title: '你好，世界', content: '第一篇示例文章', date: '2025-12-23' }
])

const filteredPosts = computed(() => {
  return posts.value.filter(p => {
    const matchesKeyword = props.search
      ? p.title.includes(props.search) || p.content.includes(props.search)
      : true
    const matchesDate = props.date
      ? p.date === props.date
      : true
    return matchesKeyword && matchesDate
  })
})
</script>

<style scoped>
.blog-main {
  margin: 0 auto;
  max-width: 740px;
  background: transparent;
}

.blog-title {
  font-size: 2.0em;
  font-weight: bold;
  color: #fff;
  margin: 32px 0 24px 0;
}

.post-card {
  background: #23242a;
  border-radius: 12px;
  margin-bottom: 32px;
  padding: 24px 28px;
  box-shadow: 0 2px 12px #0002;
}

.post-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.post-title {
  font-size: 1.4em;
  font-weight: 700;
  color: #2fd283;
}

.post-date {
  color: #aaa;
  font-size: 0.96em;
}

.post-content {
  color: #fff;
  margin-top: 18px;
  font-size: 1.12em;
}

.post-divider {
  height: 1px;
  background: #333;
  margin: 18px 0 0 0;
  opacity: 0.6;
}
</style>