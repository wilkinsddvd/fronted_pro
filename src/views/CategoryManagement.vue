<template>
  <div class="category-management">
    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <span>分类管理</span>
          <el-button type="primary" @click="handleCreate">新建分类</el-button>
        </div>
      </template>
      
      <div v-loading="loading">
        <el-table :data="categories" stripe style="width: 100%">
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="name" label="分类名称" min-width="200" />
          <el-table-column prop="description" label="描述" min-width="300" />
          <el-table-column prop="ticketCount" label="工单数量" width="120" />
          <el-table-column prop="createTime" label="创建时间" width="180" />
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
import { getCategories } from '@/api/index.js'

const categories = ref([])
const loading = ref(false)
const error = ref('')

const fetchCategories = async () => {
  loading.value = true
  error.value = ''
  try {
    const res = await getCategories()
    if (res && res.data) {
      categories.value = res.data.items || res.data.list || res.data || []
    }
  } catch (err) {
    console.error('获取分类列表失败:', err)
    error.value = '获取分类列表失败: ' + (err.message || '网络错误')
  } finally {
    loading.value = false
  }
}

const handleCreate = () => {
  ElMessage.info('创建分类功能开发中')
}

const handleEdit = (row) => {
  ElMessage.info(`编辑分类 #${row.id}`)
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确认删除该分类吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    ElMessage.success('删除成功')
    fetchCategories()
  } catch (err) {
    if (err !== 'cancel') {
      ElMessage.error('删除失败: ' + (err.message || '网络错误'))
    }
  }
}

onMounted(() => {
  fetchCategories()
})
</script>

<style scoped>
.category-management {
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
