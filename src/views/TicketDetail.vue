<template>
  <div class="ticket-detail">
    <el-card shadow="hover" v-loading="loading">
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <el-button :icon="ArrowLeft" @click="handleBack">返回</el-button>
            <span class="title">工单详情 #{{ ticketId }}</span>
          </div>
          <div class="header-right">
            <el-button type="primary" @click="handleEdit">编辑</el-button>
          </div>
        </div>
      </template>

      <div v-if="ticket" class="detail-content">
        <!-- 基本信息 -->
        <el-descriptions title="基本信息" :column="2" border>
          <el-descriptions-item label="标题">
            {{ ticket.title }}
          </el-descriptions-item>
          <el-descriptions-item label="状态">
            <TicketStatusTag :status="ticket.status" />
          </el-descriptions-item>
          <el-descriptions-item label="优先级">
            <el-tag v-if="ticket.priority === 'high'" type="danger">高</el-tag>
            <el-tag v-else-if="ticket.priority === 'medium'" type="warning">中</el-tag>
            <el-tag v-else type="info">低</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="分类">
            {{ getCategoryLabel(ticket.category) }}
          </el-descriptions-item>
          <el-descriptions-item label="创建时间">
            {{ ticket.createdAt }}
          </el-descriptions-item>
          <el-descriptions-item label="更新时间">
            {{ ticket.updatedAt }}
          </el-descriptions-item>
          <el-descriptions-item label="创建人">
            {{ ticket.creator || '未知' }}
          </el-descriptions-item>
          <el-descriptions-item label="处理人">
            {{ ticket.assignee || '未分配' }}
          </el-descriptions-item>
          <el-descriptions-item label="描述" :span="2">
            <div class="description">{{ ticket.description }}</div>
          </el-descriptions-item>
        </el-descriptions>

        <!-- 流程信息 -->
        <div class="section" v-if="ticket.workflow && ticket.workflow.length">
          <h3>流程记录</h3>
          <el-timeline>
            <el-timeline-item
              v-for="item in ticket.workflow"
              :key="item.id"
              :timestamp="item.createdAt"
              placement="top"
            >
              <el-card>
                <p><strong>{{ item.action }}</strong></p>
                <p v-if="item.operator">操作人: {{ item.operator }}</p>
                <p v-if="item.comment">备注: {{ item.comment }}</p>
              </el-card>
            </el-timeline-item>
          </el-timeline>
        </div>

        <!-- 历史记录 -->
        <div class="section" v-if="ticket.history && ticket.history.length">
          <h3>变更历史</h3>
          <el-table :data="ticket.history" stripe style="width: 100%">
            <el-table-column prop="field" label="字段" width="120" />
            <el-table-column prop="oldValue" label="原值" min-width="150" />
            <el-table-column prop="newValue" label="新值" min-width="150" />
            <el-table-column prop="operator" label="操作人" width="120" />
            <el-table-column prop="createdAt" label="时间" width="180" />
          </el-table>
        </div>

        <!-- 回复区域（预留） -->
        <div class="section">
          <h3>回复</h3>
          <el-empty description="回复功能即将上线" />
        </div>
      </div>
    </el-card>

    <!-- 编辑表单 -->
    <TicketForm
      v-model:visible="formVisible"
      :ticket="ticket"
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
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ArrowLeft } from '@element-plus/icons-vue'
import TicketStatusTag from '@/components/ticket/TicketStatusTag.vue'
import TicketForm from '@/components/ticket/TicketForm.vue'
import { getTicket, updateTicket } from '@/api/index.js'

const route = useRoute()
const router = useRouter()

const ticket = ref(null)
const loading = ref(false)
const error = ref('')
const formVisible = ref(false)

const ticketId = computed(() => route.params.id)

const categoryLabels = {
  'technical': '技术支持',
  'after_sales': '售后服务',
  'product': '产品咨询',
  'other': '其他'
}

const getCategoryLabel = (category) => {
  return categoryLabels[category] || category
}

const fetchTicket = async () => {
  loading.value = true
  error.value = ''
  try {
    const res = await getTicket(ticketId.value)
    if (res && res.data) {
      ticket.value = res.data
    }
  } catch (err) {
    console.error('获取工单详情失败:', err)
    error.value = '获取工单详情失败: ' + (err.message || '网络错误')
  } finally {
    loading.value = false
  }
}

const handleBack = () => {
  router.back()
}

const handleEdit = () => {
  formVisible.value = true
}

const handleSubmit = async (data) => {
  try {
    await updateTicket(data.id, data)
    ElMessage.success('更新成功')
    fetchTicket()
  } catch (err) {
    ElMessage.error('更新失败: ' + (err.message || '网络错误'))
    throw err
  }
}

onMounted(() => {
  fetchTicket()
})
</script>

<style scoped>
.ticket-detail {
  animation: fadeIn 0.3s ease-in;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.title {
  font-size: 18px;
  font-weight: 600;
}

.detail-content {
  padding: 0;
}

.description {
  white-space: pre-wrap;
  line-height: 1.6;
}

.section {
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid #e4e7ed;
}

.section h3 {
  margin-bottom: 16px;
  font-size: 16px;
  font-weight: 600;
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
