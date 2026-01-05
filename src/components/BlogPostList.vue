<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { getPosts } from '@/api/index.js'
import BlogPostItem from './BlogPostItem.vue'

const props = defineProps({
  search: String,
  date: String
})

const route = useRoute()
const posts = ref([])
const loading = ref(false)
const error = ref('')
const page = ref(1)
const size = ref(10)
const total = ref(0)

// 加载文章列表
async function loadPosts() {
  loading.value = true
  error.value = ''
  try {
    const params = {
      page: page.value,
      size: size.value
    }
    if (props.search) {
      params.search = props.search
    }
    if (props.date) {
      params.date = props.date
    }
    // 支持从URL查询参数获取分类和标签过滤
    if (route.query.category) {
      params.category = route.query.category
    }
    if (route.query.tag) {
      params.tag = route.query.tag
    }
    
    const res = await getPosts(params)
    posts.value = res.data.posts || []
    total.value = res.data.total || 0
  } catch (e) {
    error.value = '加载文章列表失败: ' + e.message
    console.error(e)
  } finally {
    loading.value = false
  }
}

// 切换页码
function changePage(newPage) {
  page.value = newPage
  loadPosts()
}

// 监听搜索、日期和路由查询参数变化
watch(() => [props.search, props.date, route.query.category, route.query.tag], () => {
  page.value = 1
  loadPosts()
})

onMounted(() => {
  loadPosts()
})
</script>

<template>
  <section class="post-list-container">
    <h2>
      文章列表
      <span v-if="route.query.category" class="filter-tag">分类: {{ route.query.category }}</span>
      <span v-if="route.query.tag" class="filter-tag">标签: {{ route.query.tag }}</span>
    </h2>
    
    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else-if="posts.length === 0" class="empty">暂无文章</div>
    <div v-else>
      <BlogPostItem v-for="post in posts" :key="post.id" :post="post"/>
      
      <!-- 分页 -->
      <div class="pagination" v-if="total > size">
        <button 
          @click="changePage(page - 1)" 
          :disabled="page <= 1"
          class="page-btn"
        >上一页</button>
        <span class="page-info">第 {{ page }} 页 / 共 {{ Math.ceil(total / size) }} 页</span>
        <button 
          @click="changePage(page + 1)" 
          :disabled="page >= Math.ceil(total / size)"
          class="page-btn"
        >下一页</button>
      </div>
    </div>
  </section>
</template>

<style scoped>
.post-list-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

h2 {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.filter-tag {
  font-size: 0.8em;
  background: #007bff;
  color: white;
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
}

.loading, .error, .empty {
  text-align: center;
  padding: 2rem;
  font-size: 1.1rem;
}

.error {
  color: #e74c3c;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 2rem;
  padding: 1rem;
}

.page-btn {
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  background: #fff;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.page-btn:hover:not(:disabled) {
  background: #007bff;
  color: #fff;
  border-color: #007bff;
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-info {
  color: #666;
}
</style>