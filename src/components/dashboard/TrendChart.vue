<template>
  <el-card class="trend-chart-card" shadow="hover">
    <template #header>
      <div class="card-header">
        <span>工单趋势</span>
        <el-radio-group v-model="timeRange" size="small" @change="handleRangeChange">
          <el-radio-button label="week">最近7天</el-radio-button>
          <el-radio-button label="month">最近30天</el-radio-button>
        </el-radio-group>
      </div>
    </template>
    <div v-loading="loading" class="chart-container">
      <div ref="chartRef" style="width: 100%; height: 100%;"></div>
    </div>
  </el-card>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import * as echarts from 'echarts'

const props = defineProps({
  data: {
    type: Object,
    default: () => ({
      dates: [],
      newTickets: [],
      completedTickets: []
    })
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['rangeChange'])

const chartRef = ref(null)
const timeRange = ref('week')
let chartInstance = null

// Chart color configuration
const CHART_COLORS = {
  new: {
    primary: '#409EFF',
    gradient: ['rgba(64, 158, 255, 0.3)', 'rgba(64, 158, 255, 0.05)']
  },
  completed: {
    primary: '#67C23A',
    gradient: ['rgba(103, 194, 58, 0.3)', 'rgba(103, 194, 58, 0.05)']
  }
}

const initChart = () => {
  if (!chartRef.value) return
  
  chartInstance = echarts.init(chartRef.value)
  updateChart()
}

const updateChart = () => {
  if (!chartInstance) return
  
  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross'
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
      boundaryGap: false,
      data: props.data.dates || []
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        name: '新增工单',
        type: 'line',
        smooth: true,
        data: props.data.newTickets || [],
        itemStyle: {
          color: CHART_COLORS.new.primary
        },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: CHART_COLORS.new.gradient[0] },
            { offset: 1, color: CHART_COLORS.new.gradient[1] }
          ])
        }
      },
      {
        name: '完成工单',
        type: 'line',
        smooth: true,
        data: props.data.completedTickets || [],
        itemStyle: {
          color: CHART_COLORS.completed.primary
        },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: CHART_COLORS.completed.gradient[0] },
            { offset: 1, color: CHART_COLORS.completed.gradient[1] }
          ])
        }
      }
    ]
  }
  
  chartInstance.setOption(option)
}

const handleRangeChange = () => {
  emit('rangeChange', timeRange.value)
}

onMounted(async () => {
  await nextTick()
  initChart()
  
  // Resize chart after initialization to match container
  setTimeout(() => {
    chartInstance?.resize()
  }, 200)
  
  window.addEventListener('resize', () => {
    chartInstance?.resize()
  })
})

onUnmounted(() => {
  chartInstance?.dispose()
})

watch(() => props.data, () => {
  updateChart()
}, { deep: true })
</script>

<style scoped>
.trend-chart-card {
  border-radius: 8px;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.chart-container {
  flex: 1;
  width: 100%;
  min-height: 0;
  display: flex;
}

.chart-container > div {
  flex: 1;
  min-height: 0;
}
</style>
