<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { marked } from 'marked'
import hljs from 'highlight.js'
import 'highlight.js/styles/atom-one-light.css'
import { getPost, addPostView, addPostLike } from '@/api/index.js'
import { showMessage } from '@/utils/message.js'

const route = useRoute()
const content = ref('')
const title = ref('')
const date = ref('')
const tags = ref([])
const category = ref('')
const author = ref('')
const views = ref(0)
const loading = ref(false)
const error = ref('')

// 配置marked
marked.setOptions({
  highlight: code => hljs.highlightAuto(code).value
})

async function loadPost() {
  loading.value = true
  error.value = ''
  // Note: route.params.slug contains the post ID 
  // (parameter name 'slug' is kept for backward compatibility with existing URLs)
  const postId = route.params.slug
  
  try {
    const res = await getPost(postId)
    const post = res.data
    
    title.value = post.title || ''
    date.value = post.date || ''
    tags.value = post.tags || []
    category.value = post.category || ''
    author.value = post.author || ''
    views.value = post.views || 0
    content.value = marked.parse(post.content || '')
    
    // 增加浏览量
    await addPostView(postId).catch(err => {
      console.error('Failed to add view:', err)
    })
    views.value++
  } catch (e) {
    error.value = '加载文章失败: ' + e.message
    content.value = '<p>未找到此文章。</p>'
  } finally {
    loading.value = false
  }
}

async function handleLike() {
  const postId = route.params.slug
  try {
    await addPostLike(postId)
    showMessage('点赞成功！', 'success')
  } catch (e) {
    console.error('Failed to like:', e)
    showMessage('点赞失败: ' + e.message, 'error')
  }
}

onMounted(() => {
  loadPost()
})
</script>

<template>
  <article class="post-detail">
    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else>
      <h1>{{ title }}</h1>
      <div v-if="date || tags.length || category || author" class="meta">
        <time v-if="date">{{ date }}</time>
        <span v-if="category" class="category">{{ category }}</span>
        <span v-if="author" class="author">作者: {{ author }}</span>
        <span class="views">浏览: {{ views }}</span>
        <ul class="tags" v-if="tags.length">
          <li v-for="t in tags" :key="t">#{{ t }}</li>
        </ul>
      </div>
      <div v-html="content" class="markdown-body"></div>
      <div class="actions">
        <button @click="handleLike" class="like-btn">👍 点赞</button>
      </div>
    </div>
  </article>
</template>

<style scoped>
.post-detail {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.loading, .error {
  text-align: center;
  padding: 2rem;
  font-size: 1.1rem;
}

.error {
  color: #e74c3c;
}

.markdown-body img {
  max-width: 100%;
}

.meta {
  margin-bottom: 1rem;
  color: #888;
  font-size: 0.96em;
  display: flex;
  gap: 1.5em;
  align-items: center;
  flex-wrap: wrap;
}

.meta .tags {
  list-style: none;
  display: flex;
  gap: 0.5em;
  margin: 0;
  padding: 0;
}

.meta .category {
  background: #eef6f5;
  color: #249d8f;
  padding: 0 0.5em;
  border-radius: 0.5em;
  font-size: 0.94em;
}

.actions {
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid #eee;
  display: flex;
  gap: 1rem;
}

.like-btn {
  padding: 0.5rem 1.5rem;
  background: #ff6b6b;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background 0.2s;
}

.like-btn:hover {
  background: #ee5a52;
}
</style>