<template>
  <el-table
    :data="tickets"
    :loading="loading"
    stripe
    style="width: 100%"
    @row-click="handleRowClick"
  >
    <el-table-column prop="id" label="ID" width="80" />
    <el-table-column prop="title" label="标题" min-width="200" show-overflow-tooltip />
    <el-table-column prop="status" label="状态" width="120">
      <template #default="{ row }">
        <TicketStatusTag :status="row.status" />
      </template>
    </el-table-column>
    <el-table-column prop="priority" label="优先级" width="100">
      <template #default="{ row }">
        <el-tag v-if="row.priority === 'high'" type="danger" size="small">高</el-tag>
        <el-tag v-else-if="row.priority === 'medium'" type="warning" size="small">中</el-tag>
        <el-tag v-else type="info" size="small">低</el-tag>
      </template>
    </el-table-column>
    <el-table-column prop="category" label="分类" width="120" />
    <el-table-column prop="assignee" label="处理人" width="120" />
    <el-table-column prop="createdAt" label="创建时间" width="180" />
    <el-table-column label="操作" width="240" fixed="right">
      <template #default="{ row }">
        <el-button size="small" @click.stop="handleView(row)">查看</el-button>
        <el-button size="small" type="primary" @click.stop="handleEdit(row)">编辑</el-button>
        <el-button size="small" type="danger" @click.stop="handleDelete(row)">删除</el-button>
      </template>
    </el-table-column>
  </el-table>
</template>

<script setup>
import TicketStatusTag from './TicketStatusTag.vue'

defineProps({
  tickets: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['view', 'edit', 'delete', 'row-click'])

const handleView = (row) => {
  emit('view', row)
}

const handleEdit = (row) => {
  emit('edit', row)
}

const handleDelete = (row) => {
  emit('delete', row)
}

const handleRowClick = (row) => {
  emit('row-click', row)
}
</script>
