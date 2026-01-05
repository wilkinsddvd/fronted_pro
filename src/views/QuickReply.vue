<template>
  <div class="quick-reply">
    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <span>快速回复模板</span>
          <el-button type="primary" @click="handleCreate">新建模板</el-button>
        </div>
      </template>
      
      <div v-loading="loading">
        <el-table :data="replies" stripe style="width: 100%">
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="title" label="标题" width="200" />
          <el-table-column prop="content" label="内容" min-width="300" show-overflow-tooltip />
          <el-table-column prop="category" label="分类" width="120" />
          <el-table-column prop="useCount" label="使用次数" width="120" />
          <el-table-column label="操作" width="180" fixed="right">
            <template #default="{ row }">
              <el-button size="small" type="primary" @click="handleEdit(row)">编辑</el-button>
              <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>

    <el-alert
      v-if="error"
      :title="error"
      type="error"
      show-icon
      :closable="false"
      style="margin-top: 20px;"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getQuickReplies, deleteQuickReply } from '@/api/index.js'

const replies = ref([])
const loading = ref(false)
const error = ref('')

const fetchReplies = async () => {
  loading.value = true
  error.value = ''
  try {
    const res = await getQuickReplies()
    if (res && res.data) {
      replies.value = res.data.items || res.data.list || res.data || []
    }
  } catch (err) {
    console.error('获取快速回复列表失败:', err)
    error.value = '获取快速回复列表失败: ' + (err.message || '网络错误')
  } finally {
    loading.value = false
  }
}

const handleCreate = () => {
  ElMessage.info('创建快速回复功能开发中')
}

const handleEdit = (row) => {
  ElMessage.info(`编辑快速回复 #${row.id}`)
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确认删除该快速回复吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await deleteQuickReply(row.id)
    ElMessage.success('删除成功')
    fetchReplies()
  } catch (err) {
    if (err !== 'cancel') {
      ElMessage.error('删除失败: ' + (err.message || '网络错误'))
    }
  }
}

onMounted(() => {
  fetchReplies()
})
</script>

<style scoped>
.quick-reply {
  animation: fadeIn 0.3s ease-in;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
