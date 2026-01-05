<template>
  <div class="dashboard">
    <!-- 统计卡片 -->
    <StatsCards :stats="statsData" />

    <!-- 图表区域 -->
    <el-row :gutter="20">
      <el-col :xs="24" :lg="16">
        <TrendChart 
          :data="trendData" 
          :loading="trendLoading"
          @rangeChange="handleRangeChange" 
        />
      </el-col>
      <el-col :xs="24" :lg="8">
        <CategoryPie 
          :data="categoryData" 
          :loading="categoryLoading"
        />
      </el-col>
    </el-row>

    <!-- 错误提示 -->
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
import { ElMessage } from 'element-plus'
import StatsCards from '@/components/dashboard/StatsCards.vue'
import TrendChart from '@/components/dashboard/TrendChart.vue'
import CategoryPie from '@/components/dashboard/CategoryPie.vue'
import { getDashboardStats, getTicketTrend, getCategoryStats } from '@/api/index.js'
import { DocumentAdd, Loading, SuccessFilled, WarnTriangleFilled } from '@element-plus/icons-vue'

const statsData = ref([
  {
    key: 'new',
    label: '新增工单',
    value: 0,
    trend: 0,
    color: '#409EFF',
    icon: DocumentAdd
  },
  {
    key: 'processing',
    label: '处理中',
    value: 0,
    trend: 0,
    color: '#E6A23C',
    icon: Loading
  },
  {
    key: 'completed',
    label: '已完成',
    value: 0,
    trend: 0,
    color: '#67C23A',
    icon: SuccessFilled
  },
  {
    key: 'overdue',
    label: '逾期',
    value: 0,
    trend: 0,
    color: '#F56C6C',
    icon: WarnTriangleFilled
  }
])

const trendData = ref({
  dates: [],
  newTickets: [],
  completedTickets: []
})

const categoryData = ref([])
const trendLoading = ref(false)
const categoryLoading = ref(false)
const error = ref('')

// 获取仪表盘统计数据
const fetchDashboardStats = async () => {
  try {
    const res = await getDashboardStats()
    if (res && res.data) {
      const data = res.data
      // 更新统计卡片数据
      statsData.value = [
        {
          key: 'new',
          label: '新增工单',
          value: data.newTickets || 0,
          trend: data.newTicketsTrend || 0,
          color: '#409EFF',
          icon: DocumentAdd
        },
        {
          key: 'processing',
          label: '处理中',
          value: data.processingTickets || 0,
          trend: data.processingTicketsTrend || 0,
          color: '#E6A23C',
          icon: Loading
        },
        {
          key: 'completed',
          label: '已完成',
          value: data.completedTickets || 0,
          trend: data.completedTicketsTrend || 0,
          color: '#67C23A',
          icon: SuccessFilled
        },
        {
          key: 'overdue',
          label: '逾期',
          value: data.overdueTickets || 0,
          trend: data.overdueTicketsTrend || 0,
          color: '#F56C6C',
          icon: WarnTriangleFilled
        }
      ]
    }
  } catch (err) {
    console.error('获取统计数据失败:', err)
    error.value = '获取统计数据失败: ' + (err.message || '网络错误')
  }
}

// 获取趋势数据
const fetchTrendData = async (range = 'week') => {
  trendLoading.value = true
  try {
    const res = await getTicketTrend({ range })
    if (res && res.data) {
      trendData.value = {
        dates: res.data.dates || [],
        newTickets: res.data.newTickets || [],
        completedTickets: res.data.completedTickets || []
      }
    }
  } catch (err) {
    console.error('获取趋势数据失败:', err)
    error.value = '获取趋势数据失败: ' + (err.message || '网络错误')
  } finally {
    trendLoading.value = false
  }
}

// 获取分类统计数据
const fetchCategoryStats = async () => {
  categoryLoading.value = true
  try {
    const res = await getCategoryStats()
    if (res && res.data) {
      categoryData.value = res.data.map(item => ({
        name: item.name || item.category,
        value: item.value || item.count
      }))
    }
  } catch (err) {
    console.error('获取分类统计失败:', err)
    error.value = '获取分类统计失败: ' + (err.message || '网络错误')
  } finally {
    categoryLoading.value = false
  }
}

// 处理时间范围变化
const handleRangeChange = (range) => {
  fetchTrendData(range)
}

// 初始化数据
onMounted(() => {
  fetchDashboardStats()
  fetchTrendData()
  fetchCategoryStats()
})
</script>

<style scoped>
.dashboard {
  animation: fadeIn 0.3s ease-in;
  display: flex;
  flex-direction: column;
  height: 100%;
  min-height: 0;
}

.dashboard :deep(.el-row) {
  flex: 1;
  min-height: 0;
}

.dashboard > :deep(.el-row:last-of-type) {
  display: flex;
  flex: 1;
  min-height: 0;
}

.dashboard > :deep(.el-row:last-of-type .el-col) {
  display: flex;
  flex-direction: column;
  min-height: 0;
}

.dashboard :deep(.trend-chart-card),
.dashboard :deep(.category-pie-card) {
  display: flex;
  flex-direction: column;
  height: 100%;
  margin-bottom: 0;
}

.dashboard :deep(.el-card__body) {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
  padding: 20px;
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

/* Responsive adjustments */
@media (max-width: 768px) {
  .dashboard :deep(.el-col) {
    margin-bottom: 12px;
  }
}
</style>
