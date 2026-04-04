<template>
  <div class="dashboard">
    <!-- 页面头部：刷新按钮 -->
    <div class="dashboard-header">
      <el-button
        :loading="statsLoading || trendLoading || categoryLoading"
        :icon="Refresh"
        circle
        @click="refreshData"
        title="刷新数据"
      />
    </div>

    <!-- 统计卡片 -->
    <StatsCards :stats="statsData" :loading="statsLoading" />

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
      closable
      @close="error = ''"
      style="margin-top: 20px;"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, markRaw } from 'vue'
import StatsCards from '@/components/dashboard/StatsCards.vue'
import TrendChart from '@/components/dashboard/TrendChart.vue'
import CategoryPie from '@/components/dashboard/CategoryPie.vue'
import { getDashboardStats, getTicketTrend, getCategoryStats } from '@/api/index.js'
import { DocumentAdd, Tickets, SuccessFilled, WarnTriangleFilled, Refresh } from '@element-plus/icons-vue'

const statsData = ref([
  {
    key: 'new',
    label: '新增工单',
    value: 0,
    trend: null,
    color: '#409EFF',
    icon: markRaw(DocumentAdd)
  },
  {
    key: 'total',
    label: '工单总数',
    value: 0,
    trend: null,
    color: '#E6A23C',
    icon: markRaw(Tickets)
  },
  {
    key: 'completed',
    label: '已完成',
    value: 0,
    trend: null,
    color: '#67C23A',
    icon: markRaw(SuccessFilled)
  },
  {
    key: 'overdue',
    label: '逾期',
    value: 0,
    trend: null,
    color: '#F56C6C',
    icon: markRaw(WarnTriangleFilled)
  }
])

const trendData = ref({
  dates: [],
  newTickets: [],
  completedTickets: []
})

const categoryData = ref([])
const statsLoading = ref(false)
const trendLoading = ref(false)
const categoryLoading = ref(false)
const error = ref('')

// 获取仪表盘统计数据
const fetchDashboardStats = async () => {
  statsLoading.value = true
  error.value = ''
  try {
    const res = await getDashboardStats()
    if (res && res.data) {
      const data = res.data
      statsData.value = [
        {
          key: 'new',
          label: '新增工单',
          value: data.newTickets ?? 0,
          trend: data.newTicketsTrend ?? null,
          color: '#409EFF',
          icon: markRaw(DocumentAdd)
        },
        {
          key: 'total',
          label: '工单总数',
          value: data.totalTickets ?? 0,
          // 后端暂不提供总工单数的趋势数据
          trend: null,
          color: '#E6A23C',
          icon: markRaw(Tickets)
        },
        {
          key: 'completed',
          label: '已完成',
          value: data.completedTickets ?? 0,
          trend: data.completedTicketsTrend ?? null,
          color: '#67C23A',
          icon: markRaw(SuccessFilled)
        },
        {
          key: 'overdue',
          label: '逾期',
          value: data.overdueTickets ?? 0,
          trend: data.overdueTicketsTrend ?? null,
          color: '#F56C6C',
          icon: markRaw(WarnTriangleFilled)
        }
      ]
    }
  } catch (err) {
    console.error('获取统计数据失败:', err)
    error.value = '获取统计数据失败，请稍后重试'
  } finally {
    statsLoading.value = false
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
    trendData.value = { dates: [], newTickets: [], completedTickets: [] }
    error.value = '获取趋势数据失败，请稍后重试'
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
    categoryData.value = []
    error.value = '获取分类统计失败，请稍后重试'
  } finally {
    categoryLoading.value = false
  }
}

// 刷新所有数据
const refreshData = () => {
  fetchDashboardStats()
  fetchTrendData()
  fetchCategoryStats()
}

// 处理时间范围变化
const handleRangeChange = (range) => {
  fetchTrendData(range)
}

// 初始化数据
onMounted(() => {
  refreshData()
})
</script>

<style scoped>
.dashboard {
  animation: fadeIn 0.3s ease-in;
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  min-height: 0;
}

/* Stats cards row - fixed height */
.dashboard > :deep(.el-row:first-of-type) {
  flex-shrink: 0;
  margin-bottom: 20px;
}

/* Charts row - flexible height */
.dashboard > :deep(.el-row:nth-child(2)) {
  display: flex;
  flex: 1;
  min-height: 0;
  margin-bottom: 0;
}

.dashboard > :deep(.el-row:nth-child(2) .el-col) {
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

.dashboard :deep(.trend-chart-card .el-card__body),
.dashboard :deep(.category-pie-card .el-card__body) {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
  padding: 20px;
}

/* Error alert - fixed at bottom */
.dashboard > :deep(.el-alert) {
  flex-shrink: 0;
  margin-top: 20px;
}

.dashboard-header {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 12px;
  flex-shrink: 0;
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
  
  .dashboard > :deep(.el-row:nth-child(2)) {
    flex-direction: column;
  }
}
</style>
