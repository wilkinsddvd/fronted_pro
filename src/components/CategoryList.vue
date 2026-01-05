<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getCategories } from '@/api/index.js'

const categories = ref([])
const loading = ref(false)
const error = ref('')
const router = useRouter()

async function loadCategories() {
  loading.value = true
  error.value = ''
  try {
    const res = await getCategories()
    categories.value = res.data.categories || []
  } catch (e) {
    error.value = '加载分类失败: ' + e.message
    console.error(e)
  } finally {
    loading.value = false
  }
}

function viewCategory(categoryName) {
  router.push({
    path: '/',
    query: { category: categoryName }
  })
}

onMounted(() => {
  loadCategories()
})
</script>

<template>
  <section class="category-list">
    <h2>全部分类</h2>
    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else-if="categories.length === 0" class="empty">暂无分类</div>
    <ul v-else>
      <li v-for="c in categories" :key="c.name" @click="viewCategory(c.name)" class="category-item">
        {{ c.name }} ({{ c.count }})
      </li>
    </ul>
  </section>
</template>

<style scoped>
.category-list {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.loading, .error, .empty {
  text-align: center;
  padding: 2rem;
  font-size: 1.1rem;
}

.error {
  color: #e74c3c;
}

ul {
  list-style: none;
  padding: 0;
}

.category-item {
  padding: 0.8rem 1rem;
  margin-bottom: 0.5rem;
  background: #f8f9fa;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.category-item:hover {
  background: #007bff;
  color: #fff;
  transform: translateX(5px);
}
</style>