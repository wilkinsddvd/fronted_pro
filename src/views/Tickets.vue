<template>
  <div class="tickets">
    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <span>工单列表</span>
          <el-button type="primary" @click="handleCreate">新建工单</el-button>
        </div>
      </template>

      <!-- 搜索和筛选 -->
      <el-row :gutter="20" style="margin-bottom: 20px">
        <el-col :xs="24" :sm="12" :md="8">
          <el-input
            v-model="searchQuery"
            placeholder="搜索工单标题或ID"
            clearable
            @clear="handleSearch"
            @keyup.enter="handleSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
            <template #append>
              <el-button :icon="Search" @click="handleSearch" />
            </template>
          </el-input>
        </el-col>
        <el-col :xs="24" :sm="12" :md="8">
          <el-select
            v-model="statusFilter"
            placeholder="筛选状态"
            clearable
            @change="handleSearch"
            style="width: 100%"
          >
            <el-option label="新建" value="open" />
            <el-option label="待处理" value="pending" />
            <el-option label="处理中" value="in_progress" />
            <el-option label="已解决" value="resolved" />
            <el-option label="已关闭" value="closed" />
          </el-select>
        </el-col>
        <el-col :xs="24" :sm="12" :md="8">
          <el-select
            v-model="priorityFilter"
            placeholder="筛选优先级"
            clearable
            @change="handleSearch"
            style="width: 100%"
          >
            <el-option label="高" value="high" />
            <el-option label="中" value="medium" />
            <el-option label="低" value="low" />
          </el-select>
        </el-col>
      </el-row>

      <!-- 工单表格 -->
      <TicketTable
        :tickets="tickets"
        :loading="loading"
        @view="handleView"
        @edit="handleEdit"
        @delete="handleDelete"
      />

      <!-- 分页 -->
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
    </el-card>

    <!-- 工单表单 -->
    <TicketForm
      v-model:visible="formVisible"
      :ticket="currentTicket"
      @submit="handleSubmit"
    />

    <!-- 错误提示 -->
    <el-alert
      v-if="error"
      :title="error"
      type="error"
      show-icon
      :closable="true"
      @close="error = ''"
      style="margin-top: 20px;"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search } from '@element-plus/icons-vue'
import TicketTable from '@/components/ticket/TicketTable.vue'
import TicketForm from '@/components/ticket/TicketForm.vue'
import { getTickets, createTicket, updateTicket, deleteTicket } from '@/api/index.js'

const router = useRouter()

const tickets = ref([])
const loading = ref(false)
const error = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const searchQuery = ref('')
const statusFilter = ref('')
const priorityFilter = ref('')
const formVisible = ref(false)
const currentTicket = ref(null)

const fetchTickets = async () => {
  loading.value = true
  error.value = ''
  try {
    const params = {
      page: currentPage.value,
      size: pageSize.value
    }
    
    if (searchQuery.value) {
      params.search = searchQuery.value
    }
    
    if (statusFilter.value) {
      params.status = statusFilter.value
    }
    
    if (priorityFilter.value) {
      params.priority = priorityFilter.value
    }

    const res = await getTickets(params)
    if (res && res.data) {
      tickets.value = res.data.tickets || res.data.items || res.data.list || []
      total.value = res.data.total || 0
    }
  } catch (err) {
    console.error('获取工单列表失败:', err)
    error.value = '获取工单列表失败: ' + (err.message || '网络错误')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  currentPage.value = 1
  fetchTickets()
}

const handleCreate = () => {
  currentTicket.value = null
  formVisible.value = true
}

const handleView = (row) => {
  router.push(`/tickets/${row.id}`)
}

const handleEdit = (row) => {
  currentTicket.value = { ...row }
  formVisible.value = true
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

const handleSubmit = async (data) => {
  try {
    if (data.id) {
      await updateTicket(data.id, data)
      ElMessage.success('更新成功')
    } else {
      await createTicket(data)
      ElMessage.success('创建成功')
    }
    fetchTickets()
  } catch (err) {
    ElMessage.error(`${data.id ? '更新' : '创建'}失败: ${err.message || '网络错误'}`)
    throw err
  }
}

const handleSizeChange = () => {
  currentPage.value = 1
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
