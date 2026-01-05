<template>
  <div class="stats-cards">
    <el-row :gutter="20">
      <el-col :xs="24" :sm="12" :md="6" v-for="stat in stats" :key="stat.key">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-content">
            <div class="stat-icon" :style="{ backgroundColor: stat.color }">
              <el-icon :size="28"><component :is="stat.icon" /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-label">{{ stat.label }}</div>
              <div class="stat-value">{{ stat.value }}</div>
            </div>
          </div>
          <div class="stat-footer">
            <span :class="stat.trend >= 0 ? 'trend-up' : 'trend-down'">
              {{ stat.trend >= 0 ? '↑' : '↓' }} {{ Math.abs(stat.trend) }}%
            </span>
            <span class="stat-tip">较昨日</span>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { DocumentAdd, Loading, SuccessFilled, WarnTriangleFilled } from '@element-plus/icons-vue'

defineProps({
  stats: {
    type: Array,
    default: () => [
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
    ]
  }
})
</script>

<style scoped>
.stats-cards {
  margin-bottom: 20px;
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
  margin-bottom: 16px;
}

.stat-icon {
  width: 56px;
  height: 56px;
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
  font-size: 14px;
  color: #909399;
  margin-bottom: 8px;
}

.stat-value {
  font-size: 28px;
  font-weight: 600;
  color: #303133;
}

.stat-footer {
  display: flex;
  align-items: center;
  font-size: 12px;
  padding-top: 12px;
  border-top: 1px solid #f0f0f0;
}

.trend-up {
  color: #67C23A;
  margin-right: 8px;
  font-weight: 600;
}

.trend-down {
  color: #F56C6C;
  margin-right: 8px;
  font-weight: 600;
}

.stat-tip {
  color: #909399;
}
</style>
