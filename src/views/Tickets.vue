<template>
  <div class="tickets">
    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <span>工单列表</span>
          <el-button type="primary" @click="handleCreate">新建工单</el-button>
        </div>
      </template>
      
      <div v-loading="loading">
        <el-table :data="tickets" stripe style="width: 100%">
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="title" label="标题" min-width="200" />
          <el-table-column prop="status" label="状态" width="120">
            <template #default="{ row }">
              <el-tag :type="getStatusType(row.status)">{{ row.status }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="category" label="分类" width="120" />
          <el-table-column prop="createTime" label="创建时间" width="180" />
          <el-table-column label="操作" width="180" fixed="right">
            <template #default="{ row }">
              <el-button size="small" @click="handleView(row)">查看</el-button>
              <el-button size="small" type="primary" @click="handleEdit(row)">编辑</el-button>
              <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
        
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          style="margin-top: 20px; justify-content: flex-end;"
        />
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
import { getTickets, deleteTicket } from '@/api/index.js'

const tickets = ref([])
const loading = ref(false)
const error = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

const fetchTickets = async () => {
  loading.value = true
  error.value = ''
  try {
    const res = await getTickets({
      page: currentPage.value,
      size: pageSize.value
    })
    if (res && res.data) {
      tickets.value = res.data.items || res.data.list || []
      total.value = res.data.total || 0
    }
  } catch (err) {
    console.error('获取工单列表失败:', err)
    error.value = '获取工单列表失败: ' + (err.message || '网络错误')
  } finally {
    loading.value = false
  }
}

const getStatusType = (status) => {
  const statusMap = {
    '新建': '',
    '处理中': 'warning',
    '已完成': 'success',
    '已关闭': 'info',
    '逾期': 'danger'
  }
  return statusMap[status] || ''
}

const handleCreate = () => {
  ElMessage.info('创建工单功能开发中')
}

const handleView = (row) => {
  ElMessage.info(`查看工单 #${row.id}`)
}

const handleEdit = (row) => {
  ElMessage.info(`编辑工单 #${row.id}`)
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确认删除该工单吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await deleteTicket(row.id)
    ElMessage.success('删除成功')
    fetchTickets()
  } catch (err) {
    if (err !== 'cancel') {
      ElMessage.error('删除失败: ' + (err.message || '网络错误'))
    }
  }
}

const handleSizeChange = () => {
  fetchTickets()
}

const handleCurrentChange = () => {
  fetchTickets()
}

onMounted(() => {
  fetchTickets()
})
</script>

<style scoped>
.tickets {
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
