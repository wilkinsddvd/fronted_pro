<template>
  <div class="statistics">
    <!-- Date Range Filter -->
    <el-card shadow="hover" class="filter-card">
      <el-row :gutter="20" align="middle">
        <el-col :xs="24" :sm="12" :md="8">
          <el-date-picker
            v-model="dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            @change="handleDateChange"
            style="width: 100%"
          />
        </el-col>
        <el-col :xs="24" :sm="12" :md="4">
          <el-button type="primary" @click="refreshData" :loading="refreshing">
            刷新数据
          </el-button>
        </el-col>
      </el-row>
    </el-card>

    <!-- Overview Statistics Cards -->
    <el-row :gutter="20" class="stats-overview">
      <el-col :xs="12" :sm="6" v-for="stat in overviewStats" :key="stat.key">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-content">
            <div class="stat-icon" :style="{ backgroundColor: stat.color }">
              <el-icon :size="24"><component :is="stat.icon" /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-label">{{ stat.label }}</div>
              <div class="stat-value">{{ stat.value }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- Charts Section -->
    <el-row :gutter="20">
      <!-- Status Distribution Pie Chart -->
      <el-col :xs="24" :md="12">
        <el-card shadow="hover" class="chart-card">
          <template #header>
            <span>工单状态分布</span>
          </template>
          <div v-loading="statusLoading" class="chart-container">
            <div ref="statusChartRef" style="width: 100%; height: 100%;"></div>
            <el-empty v-if="!statusLoading && statusData.length === 0" description="暂无数据" />
          </div>
        </el-card>
      </el-col>

      <!-- Priority Distribution Pie Chart -->
      <el-col :xs="24" :md="12">
        <el-card shadow="hover" class="chart-card">
          <template #header>
            <span>工单优先级分布</span>
          </template>
          <div v-loading="priorityLoading" class="chart-container">
            <div ref="priorityChartRef" style="width: 100%; height: 100%;"></div>
            <el-empty v-if="!priorityLoading && priorityData.length === 0" description="暂无数据" />
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- User Handling Stats -->
    <el-row :gutter="20">
      <el-col :span="24">
        <el-card shadow="hover" class="chart-card">
          <template #header>
            <span>用户处理工单统计</span>
          </template>
          <div v-loading="userStatsLoading" class="chart-container">
            <div ref="userStatsChartRef" style="width: 100%; height: 100%;"></div>
            <el-empty v-if="!userStatsLoading && userStatsData.length === 0" description="暂无数据" />
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- Response Time Stats -->
    <el-row :gutter="20">
      <el-col :span="24">
        <el-card shadow="hover" class="chart-card">
          <template #header>
            <span>响应时间统计</span>
          </template>
          <div v-loading="responseTimeLoading" class="chart-container">
            <div ref="responseTimeChartRef" style="width: 100%; height: 100%;"></div>
            <el-empty v-if="!responseTimeLoading && responseTimeData.length === 0" description="暂无数据" />
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- Error Alert -->
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
import { ref, onMounted, onUnmounted } from 'vue'
import { ElMessage } from 'element-plus'
import * as echarts from 'echarts'
import { 
  DocumentAdd, 
  SuccessFilled,
  Document,
  Timer
} from '@element-plus/icons-vue'
import {
  getStatisticsData,
  getTicketStatusDistribution,
  getTicketPriorityDistribution,
  getUserHandlingStats,
  getResponseTimeStats
} from '@/api/index.js'

// State
const dateRange = ref([])
const refreshing = ref(false)
const error = ref('')

// Overview stats configuration
const statsConfig = [
  { key: 'total', label: '工单总数', valueKey: 'totalTickets', color: '#409EFF', icon: Document },
  { key: 'new', label: '新增工单', valueKey: 'newTickets', color: '#E6A23C', icon: DocumentAdd },
  { key: 'completed', label: '已完成', valueKey: 'completedTickets', color: '#67C23A', icon: SuccessFilled },
  { key: 'avgTime', label: '平均响应时间(h)', valueKey: 'avgResponseTime', color: '#909399', icon: Timer }
]

const overviewStats = ref(statsConfig.map(stat => ({ ...stat, value: 0 })))

// Chart data
const statusData = ref([])
const priorityData = ref([])
const userStatsData = ref([])
const responseTimeData = ref([])

// Loading states
const statusLoading = ref(false)
const priorityLoading = ref(false)
const userStatsLoading = ref(false)
const responseTimeLoading = ref(false)

// Chart refs
const statusChartRef = ref(null)
const priorityChartRef = ref(null)
const userStatsChartRef = ref(null)
const responseTimeChartRef = ref(null)

let statusChart = null
let priorityChart = null
let userStatsChart = null
let responseTimeChart = null

// Fetch overview statistics
const fetchOverviewStats = async () => {
  try {
    const params = {}
    if (dateRange.value && dateRange.value.length === 2) {
      params.startDate = dateRange.value[0].toISOString().split('T')[0]
      params.endDate = dateRange.value[1].toISOString().split('T')[0]
    }
    
    const res = await getStatisticsData(params)
    if (res && res.data) {
      const data = res.data
      overviewStats.value = statsConfig.map(stat => ({
        ...stat,
        value: data[stat.valueKey] || 0
      }))
    }
  } catch (err) {
    console.error('获取概览统计失败:', err)
    error.value = '获取概览统计失败: ' + (err.message || '网络错误')
  }
}

// Fetch status distribution
const fetchStatusDistribution = async () => {
  statusLoading.value = true
  try {
    const res = await getTicketStatusDistribution()
    if (res && res.data) {
      statusData.value = res.data.map(item => ({
        name: item.status || item.name,
        value: item.count || item.value
      }))
      updateStatusChart()
    }
  } catch (err) {
    console.error('获取状态分布失败:', err)
    error.value = '获取状态分布失败: ' + (err.message || '网络错误')
  } finally {
    statusLoading.value = false
  }
}

// Fetch priority distribution
const fetchPriorityDistribution = async () => {
  priorityLoading.value = true
  try {
    const res = await getTicketPriorityDistribution()
    if (res && res.data) {
      priorityData.value = res.data.map(item => ({
        name: item.priority || item.name,
        value: item.count || item.value
      }))
      updatePriorityChart()
    }
  } catch (err) {
    console.error('获取优先级分布失败:', err)
    error.value = '获取优先级分布失败: ' + (err.message || '网络错误')
  } finally {
    priorityLoading.value = false
  }
}

// Fetch user handling stats
const fetchUserHandlingStats = async () => {
  userStatsLoading.value = true
  try {
    const res = await getUserHandlingStats()
    if (res && res.data) {
      userStatsData.value = res.data
      updateUserStatsChart()
    }
  } catch (err) {
    console.error('获取用户统计失败:', err)
    error.value = '获取用户统计失败: ' + (err.message || '网络错误')
  } finally {
    userStatsLoading.value = false
  }
}

// Fetch response time stats
const fetchResponseTimeStats = async () => {
  responseTimeLoading.value = true
  try {
    const params = {}
    if (dateRange.value && dateRange.value.length === 2) {
      params.startDate = dateRange.value[0].toISOString().split('T')[0]
      params.endDate = dateRange.value[1].toISOString().split('T')[0]
    }
    
    const res = await getResponseTimeStats(params)
    if (res && res.data) {
      responseTimeData.value = res.data
      updateResponseTimeChart()
    }
  } catch (err) {
    console.error('获取响应时间统计失败:', err)
    error.value = '获取响应时间统计失败: ' + (err.message || '网络错误')
  } finally {
    responseTimeLoading.value = false
  }
}

// Initialize status chart
const initStatusChart = () => {
  if (!statusChartRef.value) return
  statusChart = echarts.init(statusChartRef.value)
  updateStatusChart()
}

// Update status chart
const updateStatusChart = () => {
  if (!statusChart || statusData.value.length === 0) return
  
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      right: '10%',
      top: 'center'
    },
    series: [
      {
        name: '工单状态',
        type: 'pie',
        radius: ['40%', '70%'],
        center: ['40%', '50%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 8,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: false
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 16,
            fontWeight: 'bold'
          }
        },
        data: statusData.value
      }
    ],
    color: ['#409EFF', '#E6A23C', '#67C23A', '#F56C6C', '#909399']
  }
  
  statusChart.setOption(option)
}

// Initialize priority chart
const initPriorityChart = () => {
  if (!priorityChartRef.value) return
  priorityChart = echarts.init(priorityChartRef.value)
  updatePriorityChart()
}

// Update priority chart
const updatePriorityChart = () => {
  if (!priorityChart || priorityData.value.length === 0) return
  
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      right: '10%',
      top: 'center'
    },
    series: [
      {
        name: '优先级',
        type: 'pie',
        radius: ['40%', '70%'],
        center: ['40%', '50%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 8,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: false
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 16,
            fontWeight: 'bold'
          }
        },
        data: priorityData.value
      }
    ],
    color: ['#F56C6C', '#E6A23C', '#409EFF', '#67C23A']
  }
  
  priorityChart.setOption(option)
}

// Initialize user stats chart
const initUserStatsChart = () => {
  if (!userStatsChartRef.value) return
  userStatsChart = echarts.init(userStatsChartRef.value)
  updateUserStatsChart()
}

// Update user stats chart
const updateUserStatsChart = () => {
  if (!userStatsChart || userStatsData.value.length === 0) return
  
  const users = userStatsData.value.map(item => item.username || item.user)
  const newTickets = userStatsData.value.map(item => item.newTickets || 0)
  const completedTickets = userStatsData.value.map(item => item.completedTickets || 0)
  
  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    legend: {
      data: ['新增工单', '完成工单'],
      bottom: 0
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '50px',
      top: '20px',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: users
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        name: '新增工单',
        type: 'bar',
        data: newTickets,
        itemStyle: {
          color: '#409EFF'
        }
      },
      {
        name: '完成工单',
        type: 'bar',
        data: completedTickets,
        itemStyle: {
          color: '#67C23A'
        }
      }
    ]
  }
  
  userStatsChart.setOption(option)
}

// Initialize response time chart
const initResponseTimeChart = () => {
  if (!responseTimeChartRef.value) return
  responseTimeChart = echarts.init(responseTimeChartRef.value)
  updateResponseTimeChart()
}

// Update response time chart
const updateResponseTimeChart = () => {
  if (!responseTimeChart || responseTimeData.value.length === 0) return
  
  const dates = responseTimeData.value.map(item => item.date)
  const avgTime = responseTimeData.value.map(item => item.avgResponseTime || 0)
  const maxTime = responseTimeData.value.map(item => item.maxResponseTime || 0)
  
  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross'
      }
    },
    legend: {
      data: ['平均响应时间', '最长响应时间'],
      bottom: 0
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '50px',
      top: '20px',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: dates
    },
    yAxis: {
      type: 'value',
      name: '小时'
    },
    series: [
      {
        name: '平均响应时间',
        type: 'line',
        smooth: true,
        data: avgTime,
        itemStyle: {
          color: '#409EFF'
        },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(64, 158, 255, 0.3)' },
            { offset: 1, color: 'rgba(64, 158, 255, 0.05)' }
          ])
        }
      },
      {
        name: '最长响应时间',
        type: 'line',
        smooth: true,
        data: maxTime,
        itemStyle: {
          color: '#E6A23C'
        }
      }
    ]
  }
  
  responseTimeChart.setOption(option)
}

// Handle date change
const handleDateChange = () => {
  refreshData()
}

// Refresh all data
const refreshData = async () => {
  refreshing.value = true
  error.value = ''
  
  try {
    await Promise.allSettled([
      fetchOverviewStats(),
      fetchStatusDistribution(),
      fetchPriorityDistribution(),
      fetchUserHandlingStats(),
      fetchResponseTimeStats()
    ])
    ElMessage.success('数据刷新成功')
  } finally {
    refreshing.value = false
  }
}

// Lifecycle hooks
onMounted(() => {
  // Initialize all charts
  initStatusChart()
  initPriorityChart()
  initUserStatsChart()
  initResponseTimeChart()
  
  // Resize charts after initialization to match containers
  setTimeout(() => {
    statusChart?.resize()
    priorityChart?.resize()
    userStatsChart?.resize()
    responseTimeChart?.resize()
  }, 100)
  
  // Fetch initial data
  refreshData()
  
  // Handle window resize
  const handleResize = () => {
    statusChart?.resize()
    priorityChart?.resize()
    userStatsChart?.resize()
    responseTimeChart?.resize()
  }
  window.addEventListener('resize', handleResize)
  
  // Cleanup
  onUnmounted(() => {
    window.removeEventListener('resize', handleResize)
  })
})

onUnmounted(() => {
  statusChart?.dispose()
  priorityChart?.dispose()
  userStatsChart?.dispose()
  responseTimeChart?.dispose()
})
</script>

<style scoped>
.statistics {
  animation: fadeIn 0.3s ease-in;
  display: flex;
  flex-direction: column;
  height: 100%;
  min-height: 0;
}

.filter-card {
  margin-bottom: 20px;
  border-radius: 8px;
  flex-shrink: 0;
}

.stats-overview {
  margin-bottom: 20px;
  flex-shrink: 0;
}

.stat-card {
  border-radius: 8px;
  transition: transform 0.3s;
}

.stat-card:hover {
  transform: translateY(-4px);
}

.stat-content {
  display: flex;
  align-items: center;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  margin-right: 16px;
}

.stat-info {
  flex: 1;
}

.stat-label {
  font-size: 13px;
  color: #909399;
  margin-bottom: 6px;
}

.stat-value {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
}

.chart-card {
  margin-bottom: 20px;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
}

.chart-card :deep(.el-card__body) {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
  padding: 20px;
}

.chart-container {
  flex: 1;
  width: 100%;
  min-height: 300px;
  position: relative;
  display: flex;
}

.chart-container > div {
  flex: 1;
  min-height: 0;
}

.statistics > :deep(.el-row) {
  margin-bottom: 20px;
}

.statistics > :deep(.el-row:nth-child(3)),
.statistics > :deep(.el-row:nth-child(4)),
.statistics > :deep(.el-row:nth-child(5)) {
  flex: 1;
  min-height: 0;
  display: flex;
}

.statistics > :deep(.el-row:nth-child(3) .el-col) {
  display: flex;
  flex-direction: column;
  min-height: 0;
}

.statistics > :deep(.el-row:nth-child(4) .el-col),
.statistics > :deep(.el-row:nth-child(5) .el-col) {
  display: flex;
  flex-direction: column;
  min-height: 0;
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
