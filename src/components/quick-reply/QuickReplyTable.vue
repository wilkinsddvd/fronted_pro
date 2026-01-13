<template>
  <el-table
    :data="replies"
    :loading="loading"
    stripe
    style="width: 100%"
  >
    <el-table-column prop="id" label="ID" width="80" />
    <el-table-column prop="title" label="标题" width="200" show-overflow-tooltip />
    <el-table-column prop="content" label="内容" min-width="300" show-overflow-tooltip />
    <el-table-column prop="category" label="分类" width="120" />
    <el-table-column prop="useCount" label="使用次数" width="120" align="center" />
    <el-table-column label="操作" width="240" fixed="right">
      <template #default="{ row }">
        <el-button size="small" type="success" @click="handleCopy(row)">
          复制
        </el-button>
        <el-button size="small" type="primary" @click="handleEdit(row)">
          编辑
        </el-button>
        <el-button size="small" type="danger" @click="handleDelete(row)">
          删除
        </el-button>
      </template>
    </el-table-column>
  </el-table>
</template>

<script setup>
import { ElMessage } from 'element-plus'

defineProps({
  replies: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['edit', 'delete'])

const handleCopy = async (row) => {
  try {
    await navigator.clipboard.writeText(row.content)
    ElMessage.success('已复制到剪贴板')
  } catch (err) {
    ElMessage.error('复制失败: ' + err.message)
  }
}

const handleEdit = (row) => {
  emit('edit', row)
}

const handleDelete = (row) => {
  emit('delete', row)
}
</script>
