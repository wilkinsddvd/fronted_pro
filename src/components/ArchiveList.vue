<script setup>
import { ref, onMounted } from 'vue'
import { getArchive } from '@/api/index.js'

const archives = ref([])
const loading = ref(false)
const error = ref('')

async function loadArchive() {
  loading.value = true
  error.value = ''
  try {
    const res = await getArchive()
    archives.value = res.data.archive || []
  } catch (e) {
    error.value = '加载归档失败: ' + e.message
    console.error(e)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadArchive()
})
</script>

<template>
  <section class="archive-list">
    <h2>归档</h2>
    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else-if="archives.length === 0" class="empty">暂无归档</div>
    <div v-else>
      <div v-for="a in archives" :key="a.year" class="year-group">
        <h3>{{ a.year }}</h3>
        <ul>
          <li v-for="p in a.posts" :key="p.id">
            <router-link :to="'/post/' + p.id">{{ p.title }}</router-link> 
            <small>{{ p.date }}</small>
          </li>
        </ul>
      </div>
    </div>
  </section>
</template>

<style scoped>
.archive-list {
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

.year-group {
  margin-bottom: 2rem;
}

.year-group h3 {
  color: #007bff;
  border-bottom: 2px solid #007bff;
  padding-bottom: 0.5rem;
  margin-bottom: 1rem;
}

.year-group ul {
  list-style: none;
  padding: 0;
}

.year-group li {
  padding: 0.5rem 0;
  border-bottom: 1px dashed #eee;
}

.year-group li a {
  color: var(--color-text);
  text-decoration: none;
  margin-right: 1rem;
}

.year-group li a:hover {
  color: #007bff;
  text-decoration: underline;
}

.year-group li small {
  color: #999;
  font-size: 0.9rem;
}
</style>