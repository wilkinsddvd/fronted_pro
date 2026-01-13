<template>
  <div class="quick-reply">
    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <span>快速回复模板</span>
          <el-button type="primary" @click="handleCreate">新建模板</el-button>
        </div>
      </template>

      <!-- 搜索 -->
      <el-row :gutter="20" style="margin-bottom: 20px">
        <el-col :xs="24" :sm="12" :md="8">
          <el-input
            v-model="searchQuery"
            placeholder="搜索标题或内容"
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
            v-model="categoryFilter"
            placeholder="筛选分类"
            clearable
            @change="handleSearch"
            style="width: 100%"
          >
            <el-option label="常见问题" value="faq" />
            <el-option label="技术支持" value="technical" />
            <el-option label="售后服务" value="after_sales" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-col>
      </el-row>

      <!-- 快速回复表格 -->
      <QuickReplyTable
        :replies="replies"
        :loading="loading"
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

    <!-- 快速回复表单 -->
    <QuickReplyForm
      v-model:visible="formVisible"
      :reply="currentReply"
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
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search } from '@element-plus/icons-vue'
import QuickReplyTable from '@/components/quick-reply/QuickReplyTable.vue'
import QuickReplyForm from '@/components/quick-reply/QuickReplyForm.vue'
import { getQuickReplies, createQuickReply, updateQuickReply, deleteQuickReply } from '@/api/index.js'

const replies = ref([])
const loading = ref(false)
const error = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const searchQuery = ref('')
const categoryFilter = ref('')
const formVisible = ref(false)
const currentReply = ref(null)

const fetchReplies = async () => {
  loading.value = true
  error.value = ''
  try {
    const params = {}
    
    if (searchQuery.value) {
      params.search = searchQuery.value
    }
    
    if (categoryFilter.value) {
      params.category = categoryFilter.value
    }

    const res = await getQuickReplies(params)
    if (res && res.data) {
      // 优先从 quick_replies 字段获取数据
      const data = res.data.quick_replies || res.data.items || res.data.list || res.data || []
      
      // 字段映射函数：将 use_count 映射为 useCount
      const mapFields = (item) => {
        return {
          ...item,
          useCount: item.use_count !== undefined ? item.use_count : item.useCount
        }
      }
      
      // 如果API返回的是数组（非分页），在客户端进行分页
      if (Array.isArray(data)) {
        const mappedData = data.map(mapFields)
        const start = (currentPage.value - 1) * pageSize.value
        const end = start + pageSize.value
        replies.value = mappedData.slice(start, end)
        total.value = mappedData.length
      } else {
        // API返回分页数据
        const items = data.items || data.list || []
        replies.value = items.map(mapFields)
        total.value = data.total || 0
      }
    }
  } catch (err) {
    console.error('获取快速回复列表失败:', err)
    error.value = '获取快速回复列表失败: ' + (err.message || '网络错误')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  currentPage.value = 1
  fetchReplies()
}

const handleCreate = () => {
  currentReply.value = null
  formVisible.value = true
}

const handleEdit = (row) => {
  currentReply.value = { ...row }
  formVisible.value = true
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

const handleSubmit = async (data) => {
  try {
    if (data.id) {
      await updateQuickReply(data.id, data)
      ElMessage.success('更新成功')
    } else {
      await createQuickReply(data)
      ElMessage.success('创建成功')
    }
    fetchReplies()
  } catch (err) {
    ElMessage.error(`${data.id ? '更新' : '创建'}失败: ${err.message || '网络错误'}`)
    throw err
  }
}

const handleSizeChange = () => {
  currentPage.value = 1
  fetchReplies()
}

const handleCurrentChange = () => {
  fetchReplies()
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
