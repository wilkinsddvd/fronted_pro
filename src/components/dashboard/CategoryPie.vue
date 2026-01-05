<template>
  <el-card class="category-pie-card" shadow="hover">
    <template #header>
      <div class="card-header">
        <span>工单分类占比</span>
      </div>
    </template>
    <div v-loading="loading" class="chart-container">
      <div ref="chartRef" style="width: 100%; height: 100%;"></div>
    </div>
  </el-card>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import * as echarts from 'echarts'

const props = defineProps({
  data: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const chartRef = ref(null)
let chartInstance = null

const initChart = () => {
  if (!chartRef.value) return
  
  chartInstance = echarts.init(chartRef.value)
  updateChart()
}

const updateChart = () => {
  if (!chartInstance) return
  
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      right: '10%',
      top: 'center',
      textStyle: {
        fontSize: 12
      }
    },
    series: [
      {
        name: '工单分类',
        type: 'pie',
        radius: ['40%', '70%'],
        center: ['35%', '50%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 8,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: false,
          position: 'center'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 20,
            fontWeight: 'bold'
          }
        },
        labelLine: {
          show: false
        },
        data: props.data || []
      }
    ],
    color: ['#409EFF', '#67C23A', '#E6A23C', '#F56C6C', '#909399', '#C0C4CC']
  }
  
  chartInstance.setOption(option)
}

onMounted(() => {
  initChart()
  
  // Resize chart after initialization to match container
  setTimeout(() => {
    chartInstance?.resize()
  }, 100)
  
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
.category-pie-card {
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
