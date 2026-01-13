<template>
  <el-tag :type="tagType" :effect="effect">
    {{ statusText }}
  </el-tag>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  status: {
    type: String,
    required: true
  },
  effect: {
    type: String,
    default: 'light'
  }
})

const statusConfig = {
  'open': { text: '新建', type: '' },
  'pending': { text: '待处理', type: 'warning' },
  'in_progress': { text: '处理中', type: 'primary' },
  'resolved': { text: '已解决', type: 'success' },
  'closed': { text: '已关闭', type: 'info' },
  'rejected': { text: '已拒绝', type: 'danger' }
}

const tagType = computed(() => {
  return statusConfig[props.status]?.type || ''
})

const statusText = computed(() => {
  return statusConfig[props.status]?.text || props.status
})
</script>
