<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getTags } from '@/api/index.js'

const tags = ref([])
const loading = ref(false)
const error = ref('')
const router = useRouter()

async function loadTags() {
  loading.value = true
  error.value = ''
  try {
    const res = await getTags()
    tags.value = res.data.tags || []
  } catch (e) {
    error.value = '加载标签失败: ' + e.message
    console.error(e)
  } finally {
    loading.value = false
  }
}

function viewTag(tagName) {
  router.push({
    path: '/',
    query: { tag: tagName }
  })
}

onMounted(() => {
  loadTags()
})
</script>

<template>
  <section class="tag-list">
    <h2>标签云</h2>
    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else-if="tags.length === 0" class="empty">暂无标签</div>
    <ul v-else class="tag-cloud">
      <li v-for="t in tags" :key="t.name" @click="viewTag(t.name)" class="tag-item">
        {{ t.name }} <span class="count">({{ t.count }})</span>
      </li>
    </ul>
  </section>
</template>

<style scoped>
.tag-list {
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

.tag-cloud {
  list-style: none;
  padding: 0;
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.tag-item {
  padding: 0.5rem 1rem;
  background: #e7f3ff;
  color: #0066cc;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 0.95rem;
}

.tag-item:hover {
  background: #0066cc;
  color: #fff;
  transform: scale(1.05);
}

.count {
  font-size: 0.85rem;
  opacity: 0.8;
}
</style>